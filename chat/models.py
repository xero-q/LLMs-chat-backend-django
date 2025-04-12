from django.db import models


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {"Online" if self.is_online else "Offline"}"


class Thread(models.Model):
    title = models.CharField(max_length=255, unique=True)
    model = models.ForeignKey(
        Model, related_name='threads', on_delete=models.DO_NOTHING)

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
