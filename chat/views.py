from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Thread, Prompt, Model
from .serializers import ModelSerializer, ThreadSerializer, PromptSerializer
from .utils import OllamaChatAI


class ModelListView(ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


@api_view(['GET'])
def get_model(request, model_id):
    model = get_object_or_404(Model, pk=model_id)
    serializer = ModelSerializer(model)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadListView(ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


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

    chatai = OllamaChatAI()
    user_prompt = data.get('user_prompt')
    try:
        response = chatai.get_response(
            model=model.name, user_prompt=user_prompt)
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
