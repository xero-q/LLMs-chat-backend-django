from django.db import models
from django.db.models import OuterRef, Subquery, DateTimeField


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

    def __str__(self):
        return f"{self.id} - {self.title}"

    @property
    def first_prompt_datetime(self):
        first_prompt = self.prompts.order_by('created_at').first()
        return first_prompt.created_at if first_prompt else None

    @staticmethod
    def get_threads_ordered_by_first_prompt():
        first_prompt = Prompt.objects.filter(
            thread=OuterRef('pk')
        ).order_by('created_at')

        return Thread.objects.annotate(
            first_prompt_date=Subquery(
                first_prompt.values('created_at')[:1],
                output_field=DateTimeField()
            )
        ).order_by('-first_prompt_date')


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
