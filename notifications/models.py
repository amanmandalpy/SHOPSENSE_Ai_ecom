from django.db import models
from django.conf import settings

class NotificationType(models.TextChoices):
    PRICE_ALERT = 'PRICE_ALERT', 'Price Alert'
    STOCK_ALERT = 'STOCK_ALERT', 'Stock Alert'
    COUPON_ALERT = 'COUPON_ALERT', 'Coupon Alert'
    AI_REC = 'AI_REC', 'AI Recommendation'
    SYSTEM = 'SYSTEM', 'System Notification'

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
