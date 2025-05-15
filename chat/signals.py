from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Prompt, Thread


@receiver(post_save, sender=Prompt)
def after_save_prompt(sender, instance, created, **kwargs):
    if created:
        print(f"New object created: {instance}")
    else:
        print(f"Object updated: {instance}")


@receiver(post_delete, sender=Thread)
def after_delete_thread(sender, instance, **kwargs):
    print(f"Thread deleted: {instance}")
