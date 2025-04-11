from django.urls import path
# or ThreadListView
from .views import ThreadListView, get_prompts_for_thread, get_response_for_prompt

urlpatterns = [
    path('threads', ThreadListView.as_view()),
    path('threads/<int:thread_id>/prompts', get_prompts_for_thread),
    path('threads/<int:thread_id>/response', get_response_for_prompt),
]
