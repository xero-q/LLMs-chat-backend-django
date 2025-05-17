from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Thread, Prompt, Model, ViewThreadsMonth
from .serializers import CustomTokenObtainPairSerializer, ModelSerializer, SignupSerializer, ThreadSerializer, PromptSerializer, ViewThreadsMonthSerializer
from .aichat_factory import LangChainModel
from collections import defaultdict
from django.db.models.functions import TruncDate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import localtime
from django.utils import timezone
from zoneinfo import ZoneInfo
from django.conf import settings
import calendar


class ModelListView(ListAPIView):
    queryset = Model.objects.all().order_by('provider__name')
    serializer_class = ModelSerializer


@api_view(['GET'])
def get_model(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    serializer = ModelSerializer(model)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("pageSize", 20))

        threads = Thread.objects.filter(
            user=request.user).order_by('-created_at')

        paginator = Paginator(threads, page_size)

        try:
            paginated_threads = paginator.page(page)
        except PageNotAnInteger:
            paginated_threads = paginator.page(1)
        except EmptyPage:
            paginated_threads = paginator.page(paginator.num_pages)

        user_tz = ZoneInfo(settings.TIME_ZONE)
        utc = ZoneInfo("UTC")

        grouped = defaultdict(list)
        for thread in paginated_threads:
            created_at = thread.created_at

            if timezone.is_naive(created_at):
                created_at = created_at.replace(tzinfo=utc)

            localized_dt = created_at.astimezone(user_tz)
            date_key = localized_dt.date()

            serialized = ThreadSerializer(thread).data
            grouped[date_key].append(serialized)

        result = [
            {
                "date": datetime.combine(date, datetime.min.time()).isoformat(),
                "threads": threads
            }
            for date, threads in grouped.items()
        ]

        return Response({
            "current_page": paginated_threads.number,
            "has_next": paginated_threads.has_next(),
            "results": result
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prompts_for_thread(request, thread_id):
    prompts = Prompt.get_prompts_by_thread(thread_id)
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_response_for_prompt(request, thread_id):
    data = request.data

    thread = Thread.objects.get(id=thread_id)
    if not thread:
        return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

    aichat_model = LangChainModel(thread)

    user_prompt = data.get('user_prompt')

    try:
        response = aichat_model.get_response(user_prompt=user_prompt)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Save the prompt and response
    prompt = Prompt.objects.create(
        thread=thread,
        prompt=user_prompt,
        response=response
    )
    prompt.save()
    # Return the response
    return Response({"response": response}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_thread(request, model_id):
    data = request.data
    title = data.get('title')
    if not title:
        return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        thread = Thread.objects.create(
            model_id=model_id, title=title, user=request.user)
    except Exception as e:
        return Response({"error": "There is already a thread with this title"}, status=status.HTTP_400_BAD_REQUEST)

    thread.save()
    serializer = ThreadSerializer(thread)
    return Response({"thread": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_thread(request, thread_id):
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)
    thread.delete()
    return Response({"message": "Thread deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ListViewThreadsMonth(ListAPIView):
    queryset = ViewThreadsMonth.objects.all()
    serializer_class = ViewThreadsMonthSerializer


@api_view(['GET'])
def threads_by_month(request):
    month = int(request.query_params.get('month'))
    if not month or month < 1 or month > 12:
        return Response({"error": "Month is required (between 1 and 12)"}, status=status.HTTP_400_BAD_REQUEST)

    month_name = calendar.month_name[month]
    results = ViewThreadsMonth.objects.filter(month=month_name)
    serializer = ViewThreadsMonthSerializer(results, many=True)
    return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
