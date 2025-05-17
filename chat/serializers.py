from rest_framework import serializers
from .models import Model, Thread, Prompt, ViewThreadsMonth
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone
from django.conf import settings


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["model_type"] = instance.provider.name
        return ret


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Inject extra fields
        ret["model_name"] = instance.model.name
        ret["model_type"] = instance.model.provider.name
        ret["model_identifier"] = instance.model.identifier

        # Timezone handling
        user_tz = ZoneInfo(settings.TIME_ZONE)
        utc = ZoneInfo("UTC")

        created_at = instance.created_at
        if timezone.is_naive(created_at):
            created_at = created_at.replace(tzinfo=utc)

        local_created_at = created_at.astimezone(user_tz)
        ret["created_at_date"] = datetime.combine(
            local_created_at.date(), datetime.min.time()
            # optionally just `.date().isoformat()` if you only want the date
        ).isoformat()

        return ret


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ["prompt", "response", "created_at"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": ("The username or password is incorrect.")
    }


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ViewThreadsMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewThreadsMonth
        fields = "__all__"
