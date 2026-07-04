from django.db import models
from django.conf import settings
from affiliate.models import Merchant
from products.models import Product
from merchant_products.models import MerchantProduct
from tracking.models import Campaign

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

class MerchantAnalytics(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    total_clicks = models.IntegerField(default=0)
    unique_clicks = models.IntegerField(default=0)
    
    device_desktop = models.IntegerField(default=0)
    device_mobile = models.IntegerField(default=0)
    device_tablet = models.IntegerField(default=0)
    
    # Store JSON of country distribution
    country_distribution = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ('merchant', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.merchant.name} - {self.date}"

class ProductAnalytics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='analytics')
    
    views_count = models.IntegerField(default=0)
    search_count = models.IntegerField(default=0)
    comparison_count = models.IntegerField(default=0)
    wishlist_count = models.IntegerField(default=0)
    affiliate_clicks = models.IntegerField(default=0)
    
    ctr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Click Through Rate (%)")
    
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_ctr(self):
        if self.views_count > 0:
            self.ctr = (self.affiliate_clicks / self.views_count) * 100
        else:
            self.ctr = 0.00
        self.save(update_fields=['views_count', 'search_count', 'comparison_count', 'wishlist_count', 'affiliate_clicks', 'ctr', 'last_updated'])

    def __str__(self):
        return f"Analytics for {self.product.name}"

class CampaignAnalytics(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    total_clicks = models.IntegerField(default=0)
    unique_clicks = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('campaign', 'date')
        ordering = ['-date']
