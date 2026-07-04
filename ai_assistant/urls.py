from django.urls import path
from .views import AskAIAssistantView

urlpatterns = [
    path('', AskAIAssistantView.as_view(), name='ai_chat'),
]
