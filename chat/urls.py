from django.urls import path
from .views import ThreadListView, get_prompts_for_thread  # or ThreadListView

urlpatterns = [
    path('threads', ThreadListView.as_view()),
    path('threads/<int:thread_id>/prompts', get_prompts_for_thread),
]
