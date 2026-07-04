from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from merchant_products.models import MerchantProduct

class AlertStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    TRIGGERED = 'TRIGGERED', 'Triggered'
    EXPIRED = 'EXPIRED', 'Expired'
    PAUSED = 'PAUSED', 'Paused'
    CANCELLED = 'CANCELLED', 'Cancelled'

class AlertType(models.TextChoices):
    BELOW_TARGET = 'BELOW_TARGET', 'Price Below Target'
    ABOVE_TARGET = 'ABOVE_TARGET', 'Price Above Target'
    BACK_IN_STOCK = 'BACK_IN_STOCK', 'Back In Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out Of Stock'
    DISCOUNT_INCREASED = 'DISCOUNT_INCREASED', 'Discount Increased'

class PriceAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='price_alerts')
    merchant_product = models.ForeignKey(MerchantProduct, on_delete=models.CASCADE, related_name='alerts')
    
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    alert_type = models.CharField(max_length=20, choices=AlertType.choices, default=AlertType.BELOW_TARGET)
    status = models.CharField(max_length=20, choices=AlertStatus.choices, default=AlertStatus.ACTIVE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    triggered_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    notification_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.merchant_product.product.name} ({self.status})"

    def clean(self):
        if self.target_price < 0:
            raise ValidationError({'target_price': 'Target price cannot be negative.'})
        
        # Prevent duplicate ACTIVE alerts
        if self.status == AlertStatus.ACTIVE:
            qs = PriceAlert.objects.filter(
                user=self.user,
                merchant_product=self.merchant_product,
                status=AlertStatus.ACTIVE,
                alert_type=self.alert_type
            ).exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("You already have an active alert for this product logic.")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=90)
        super().save(*args, **kwargs)
