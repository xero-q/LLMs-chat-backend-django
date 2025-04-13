from django.db import models
from django.db.models import OuterRef, Subquery, DateTimeField
from django.db.models.functions import TruncDate
from collections import defaultdict
import datetime


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_online = models.BooleanField(default=False)
    base_url = models.CharField(max_length=255, blank=True, null=True)
    is_openai = models.BooleanField(default=False)
    api_environment_variable = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {"Online" if self.is_online else "Offline"}"


class Thread(models.Model):
    title = models.CharField(max_length=255, unique=True)
    model = models.ForeignKey(
        Model, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    @staticmethod
    def get_threads_ordered_by_created_at():
        # Aquí usamos solo el campo `created_at` para ordenar
        threads = Thread.objects.all().annotate(
            # Extraemos solo la fecha de `created_at`
            created_at_date=TruncDate('created_at')
            # Ordenamos por fecha de creación en orden descendente
        ).order_by('-created_at_date')

        # Agrupamos por fecha de creación usando defaultdict
        grouped = defaultdict(list)
        for thread in threads:
            grouped[thread.created_at_date].append(thread)

        return grouped


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
