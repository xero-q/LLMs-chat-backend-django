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
        read_only_fields = ['user', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['model_name'] = instance.model.name
        ret['is_online'] = instance.model.is_online
        return ret


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['prompt', 'response', 'created_at']
