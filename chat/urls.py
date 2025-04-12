from django.urls import path
from .views import ModelListView, ThreadListView, get_model, get_prompts_for_thread, get_response_for_prompt, start_thread, delete_thread

urlpatterns = [
    path('models', ModelListView.as_view()),
    path('models/<int:model_id>', get_model),
    path('threads', ThreadListView.as_view()),
    path('threads/<int:thread_id>/prompts', get_prompts_for_thread),
    path('threads/<int:thread_id>/response', get_response_for_prompt),
    path('threads/<int:model_id>/start', start_thread),
    path('threads/<int:thread_id>', delete_thread),
]
