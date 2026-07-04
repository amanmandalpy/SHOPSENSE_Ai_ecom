from django.db import models
from django.utils import timezone
from affiliate.models import Merchant

class FeedType(models.TextChoices):
    CSV = 'CSV', 'CSV Feed'
    XML = 'XML', 'XML Feed'
    JSON = 'JSON', 'JSON Feed'
    REST = 'REST', 'REST API'
    GRAPHQL = 'GRAPHQL', 'GraphQL API'
    ZIP = 'ZIP', 'Compressed Feed (.zip)'

class AuthType(models.TextChoices):
    NONE = 'NONE', 'No Authentication'
    BASIC = 'BASIC', 'Basic Auth (Username/Password)'
    BEARER = 'BEARER', 'Bearer Token'
    API_KEY = 'API_KEY', 'API Key'

class FeedStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    PAUSED = 'PAUSED', 'Paused'
    ERROR = 'ERROR', 'Error State'

class MerchantFeed(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='feeds')
    name = models.CharField(max_length=255, help_text="Name of the feed (e.g. 'Amazon Summer Electronics')")
    feed_type = models.CharField(max_length=20, choices=FeedType.choices, default=FeedType.CSV)
    feed_url = models.URLField(max_length=2000)
    
    # Authentication
    auth_type = models.CharField(max_length=20, choices=AuthType.choices, default=AuthType.NONE)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=1000, blank=True, null=True)
    
    # Synchronization
    status = models.CharField(max_length=20, choices=FeedStatus.choices, default=FeedStatus.INACTIVE)
    sync_frequency = models.IntegerField(default=1440, help_text="Sync frequency in minutes (default 24h)")
    last_sync = models.DateTimeField(blank=True, null=True)
    next_sync = models.DateTimeField(blank=True, null=True)
    
    # Stats (from last sync)
    total_products = models.IntegerField(default=0)
    imported_products = models.IntegerField(default=0)
    failed_products = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.merchant.name} - {self.name}"

class MerchantFeedHistory(models.Model):
    feed = models.ForeignKey(MerchantFeed, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=FeedStatus.choices)
    response_code = models.IntegerField(blank=True, null=True)
    response_time_ms = models.IntegerField(blank=True, null=True, help_text="Time taken to fetch feed in ms")
    total_products = models.IntegerField(default=0)
    imported_products = models.IntegerField(default=0)
    failed_products = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Merchant feed histories"
        
    def __str__(self):
        return f"{self.feed.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
