from django.db import models
from django.db.models import OuterRef, Subquery, DateTimeField
from django.db.models.functions import TruncDate
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ModelType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    base_url = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(
        ModelType, related_name='models', on_delete=models.CASCADE
    )
    api_environment_variable = models.CharField(
        max_length=255, blank=True, null=True)
    temperature = models.FloatField(default=0.7, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(1)
    ])

    def __str__(self):
        return f"{self.name} - ({self.type.name})"


class Thread(models.Model):
    title = models.CharField(max_length=255, unique=True)
    model = models.ForeignKey(
        Model, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True)
    user = models.ForeignKey(
        User, related_name='threads', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id} - {self.title}"


class Prompt(models.Model):
    prompt = models.TextField()
    response = models.TextField()
    thread = models.ForeignKey(
        Thread, related_name='prompts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt} - {self.created_at}"

    @staticmethod
    def get_prompts_by_thread(thread_id):
        return Prompt.objects.filter(thread_id=thread_id).order_by('created_at')
