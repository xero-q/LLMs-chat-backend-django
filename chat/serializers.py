from rest_framework import serializers
from .models import Model, Thread, Prompt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['model_type'] = instance.provider.name
        return ret


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['model_name'] = instance.model.name
        ret['model_type'] = instance.model.provider.name
        ret['model_identifier'] = instance.model.identifier
        return ret


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['prompt', 'response', 'created_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": ("The username or password is incorrect.")
    }


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
