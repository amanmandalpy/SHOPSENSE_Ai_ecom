from django.db import models
from django.conf import settings
from stores.models import Store
from merchant_products.models import MerchantProduct

class AffiliateConfig(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='affiliate_config')
    affiliate_id = models.CharField(max_length=100, help_text="e.g. shopsense-20")
    tracking_param_name = models.CharField(max_length=50, default="tag", help_text="e.g. tag or aff_id")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.store.name} Affiliate Config"

class AffiliateClick(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    merchant_product = models.ForeignKey(MerchantProduct, on_delete=models.SET_NULL, null=True)
    outbound_url = models.TextField()
    click_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=200, blank=True)
    browser = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-click_time']

    def __str__(self):
        return f"Click to {self.merchant_product} at {self.click_time}"
