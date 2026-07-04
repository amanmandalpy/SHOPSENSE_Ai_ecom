from django.db import models
from django.conf import settings
from affiliate.models import Merchant
from merchant_products.models import MerchantProduct
from products.models import Product

class UTMSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    source = models.ForeignKey(UTMSource, on_delete=models.SET_NULL, null=True, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('PAUSED', 'Paused'), ('COMPLETED', 'Completed')], default='ACTIVE')
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class ClickSession(models.Model):
    session_identifier = models.CharField(max_length=100, unique=True, help_text="Anonymous session UUID or token")
    visitor_identifier = models.CharField(max_length=100, blank=True, null=True, help_text="Long-lived visitor cookie")
    entry_page = models.URLField(max_length=1000, blank=True, null=True)
    exit_page = models.URLField(max_length=1000, blank=True, null=True)
    pages_viewed = models.IntegerField(default=0)
    session_duration = models.IntegerField(default=0, help_text="Duration in seconds")
    clicks_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.session_identifier

class AffiliateClick(models.Model):
    # Relational Data
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(ClickSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='clicks')
    merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, null=True, related_name='clicks')
    merchant_product = models.ForeignKey(MerchantProduct, on_delete=models.SET_NULL, null=True, related_name='clicks')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='affiliate_clicks')
    
    # URLs
    affiliate_url = models.TextField(help_text="The final URL with our affiliate parameters")
    original_merchant_url = models.TextField(help_text="The base URL of the merchant product")
    
    # UTMs (Incoming Traffic)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='clicks')
    
    # Network / Device Profiling
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=50, blank=True, help_text="Mobile, Tablet, Desktop")
    operating_system = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    referrer = models.TextField(blank=True)
    
    click_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-click_timestamp']
        indexes = [
            models.Index(fields=['merchant', 'click_timestamp']),
            models.Index(fields=['product', 'click_timestamp']),
            models.Index(fields=['session', 'click_timestamp']),
        ]

    def __str__(self):
        return f"Click to {self.merchant.name if self.merchant else 'Unknown'} at {self.click_timestamp}"
