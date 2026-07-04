from django.db import models

class Merchant(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Maintenance')
    ]
    
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='merchants/', blank=True, null=True)
    website = models.URLField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Capabilities
    affiliate_supported = models.BooleanField(default=True)
    official_api_supported = models.BooleanField(default=False)
    feed_supported = models.BooleanField(default=False)
    
    # Metadata
    currency = models.CharField(max_length=10, default='INR')
    country = models.CharField(max_length=10, default='IN')
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    priority = models.IntegerField(default=0, help_text="Higher priority gets synced/searched first")
    
    # Sync Status
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

class AffiliateAccount(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, related_name='affiliate_account')
    affiliate_id = models.CharField(max_length=100)
    tracking_id = models.CharField(max_length=100, blank=True)
    tracking_parameters = models.JSONField(default=dict, blank=True, help_text="e.g. {'tag': 'shopsense-20'}")
    deep_link_base_url = models.URLField(max_length=500, blank=True)
    
    COMMISSION_STATUS = [
        ('ACTIVE', 'Active'),
        ('PENDING', 'Pending'),
        ('SUSPENDED', 'Suspended')
    ]
    commission_status = models.CharField(max_length=20, choices=COMMISSION_STATUS, default='ACTIVE')
    merchant_notes = models.TextField(blank=True, help_text="TOS notes or commission rates")

    def __str__(self):
        return f"{self.merchant.name} Affiliate Account"
