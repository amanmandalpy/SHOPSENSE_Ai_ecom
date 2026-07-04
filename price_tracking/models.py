from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from merchant_products.models import MerchantProduct

class PriceHistory(models.Model):
    merchant_product = models.ForeignKey(MerchantProduct, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='INR')
    
    availability_status = models.CharField(max_length=20)
    seller_rating_snapshot = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    delivery_charge_snapshot = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cashback_snapshot = models.BooleanField(default=False)
    
    recorded_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['merchant_product', '-recorded_at']),
        ]

    def __str__(self):
        return f"{self.merchant_product.product.name} at {self.merchant_product.store.name} - {self.price} on {self.recorded_at.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})
        if self.original_price and self.original_price < self.price:
            raise ValidationError({'original_price': 'Original price must be greater than or equal to current price.'})

    def save(self, *args, **kwargs):
        self.clean()
        if self.original_price and self.price < self.original_price:
            self.discount_percentage = ((self.original_price - self.price) / self.original_price) * 100
        else:
            self.discount_percentage = 0.00
        super().save(*args, **kwargs)
