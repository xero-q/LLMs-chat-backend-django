from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Thread, Prompt
from .serializers import ThreadSerializer, PromptSerializer


class ThreadListView(ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


@api_view(['GET'])
def get_prompts_for_thread(request, thread_id):
    prompts = Prompt.get_prompts_by_thread(thread_id)
    serializer = PromptSerializer(prompts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
