from django.urls import reverse
from .models import Notification

def send_notification(user, title, message, notification_type, action_url=None):
    """
    Creates a Notification record in the database.
    Designed to be extended in the future for Email, Push, SMS APIs (e.g. Twilio, SendGrid).
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url
    )
    return notification
