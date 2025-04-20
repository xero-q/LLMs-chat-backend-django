from django.db import migrations


def insert_modeltypes(apps, schema_editor):
    ModelType = apps.get_model('chat', 'ModelType')
    names = [
        "deepseek",
        "gemini",
        "huggingface",
        "local",
        "mistral",
        "openai"
        "together"
    ]

    for name in names:
        ModelType.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_rename_type_model_provider'),
    ]

    operations = [
        migrations.RunPython(insert_modeltypes),
    ]
