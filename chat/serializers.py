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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(instance, 'first_prompt_datetime'):
            ret["first_prompt_datetime"] = instance.first_prompt_datetime
        ret['model_name'] = instance.model.name
        ret['is_online'] = instance.model.is_online
        return ret


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['prompt', 'response', 'created_at']
