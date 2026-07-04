from django.db import models
from stores.models import Store

class MerchantConnector(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='api_connector')
    api_url = models.URLField(help_text="Base URL for Merchant API")
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    last_sync_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.store.name} Connector"

class MerchantSyncLog(models.Model):
    SYNC_TYPES = [
        ('PRODUCTS', 'Products'),
        ('PRICES', 'Prices'),
        ('INVENTORY', 'Inventory'),
        ('COUPONS', 'Coupons'),
    ]
    
    connector = models.ForeignKey(MerchantConnector, on_delete=models.CASCADE, related_name='sync_logs')
    sync_type = models.CharField(max_length=50, choices=SYNC_TYPES)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('RUNNING', 'Running'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='RUNNING')
    records_processed = models.IntegerField(default=0)
    error_trace = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.connector.store.name} - {self.sync_type} at {self.start_time}"
