from django.contrib import admin

# Register your models here.
from chat.models import Model, Thread, Prompt, ModelType

# Register your models here.
admin.site.register(Model)
admin.site.register(Thread)
admin.site.register(Prompt)
admin.site.register(ModelType)
