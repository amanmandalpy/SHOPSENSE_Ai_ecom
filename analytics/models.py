from django.db import models
from django.conf import settings

class EventType(models.TextChoices):
    SEARCH = 'SEARCH', 'Search'
    PRODUCT_VIEW = 'PRODUCT_VIEW', 'Product View'
    WISHLIST_ADD = 'WISHLIST_ADD', 'Wishlist Add'
    AI_QUERY = 'AI_QUERY', 'AI Query'
    COMPARE = 'COMPARE', 'Compare'
    AFFILIATE_CLICK = 'AFFILIATE_CLICK', 'Affiliate Click'

class PlatformEvent(models.Model):
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.event_type} at {self.created_at}"
