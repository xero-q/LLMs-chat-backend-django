# Generated by Django 5.2 on 2025-04-17 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0010_modeltype_remove_model_model_type_model_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="model",
            name="type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="models",
                to="chat.modeltype",
            ),
            preserve_default=False,
        ),
    ]
