from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Thread, Prompt, Model
from .serializers import CustomTokenObtainPairSerializer, ModelSerializer, ThreadSerializer, PromptSerializer
from .utils import OnlineAIChat, OfflineAIChat, OnlineHFChat
from collections import defaultdict
from django.db.models.functions import TruncDate
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.views import TokenObtainPairView


class ModelListView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


@api_view(['GET'])
def get_model(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    serializer = ModelSerializer(model)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        threads = Thread.objects.filter(user=request.user).annotate(
            created_at_date=TruncDate('created_at')
        ).order_by('-created_at_date', '-created_at')

        grouped = defaultdict(list)
        for thread in threads:
            serialized = ThreadSerializer(thread).data
            grouped[thread.created_at_date].append(serialized)

        result = [
            {
                "date": date,
                "threads": threads
            }
            for date, threads in grouped.items()
        ]

        return Response(result)


@api_view(['GET'])
def get_prompts_for_thread(request, thread_id):
    prompts = Prompt.get_prompts_by_thread(thread_id)
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_response_for_prompt(request, thread_id):
    data = request.data

    thread = Thread.objects.get(id=thread_id)
    if not thread:
        return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get corresponding model
    model = Model.objects.get(id=thread.model_id)
    if not model:
        return Response({"error": "Model not found"}, status=status.HTTP_404_NOT_FOUND)

    if model.is_online:
        if model.is_openai:
            chat_ai = OnlineAIChat()
        else:
            chat_ai = OnlineHFChat()
    else:
        chat_ai = OfflineAIChat()

    user_prompt = data.get('user_prompt')

    try:
        response = chat_ai.get_response(
            model=model, user_prompt=user_prompt)
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
def delete_thread(request, thread_id):
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)
    thread.delete()
    return Response({"message": "Thread deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
