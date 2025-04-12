from rest_framework import serializers
from .models import Model, Thread, Prompt


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['prompt', 'response', 'created_at']
