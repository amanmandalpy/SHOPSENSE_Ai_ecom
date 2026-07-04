from django.urls import path
from .views import NotificationCenterView, mark_notification_read

urlpatterns = [
    path('', NotificationCenterView.as_view(), name='notification_center'),
    path('<int:pk>/read/', mark_notification_read, name='mark_notification_read'),
]
