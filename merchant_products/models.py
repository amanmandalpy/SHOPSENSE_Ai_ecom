from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from products.models import Product
from stores.models import Store

class StockStatus(models.TextChoices):
    IN_STOCK = 'IN_STOCK', 'In Stock'
    LIMITED_STOCK = 'LIMITED_STOCK', 'Limited Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out Of Stock'
    COMING_SOON = 'COMING_SOON', 'Coming Soon'
    DISCONTINUED = 'DISCONTINUED', 'Discontinued'

class MerchantProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='merchant_listings')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='merchant_products')
    
    # URLs
    merchant_product_url = models.URLField(max_length=500)
    merchant_sku = models.CharField(max_length=100, blank=True, null=True)
    affiliate_url = models.URLField(max_length=1000, blank=True, null=True)
    
    # Pricing
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR')
    
    # Logistics
    availability_status = models.CharField(max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    estimated_delivery_days = models.IntegerField(blank=True, null=True)
    
    # Seller Info
    seller_name = models.CharField(max_length=255, blank=True, null=True)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    # Features
    cashback_available = models.BooleanField(default=False)
    emi_available = models.BooleanField(default=False)
    cod_available = models.BooleanField(default=False)
    exchange_available = models.BooleanField(default=False)
    warranty = models.CharField(max_length=255, blank=True, null=True)
    
    # Audit
    last_synced = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'store')
        ordering = ['current_price']

    def __str__(self):
        return f"{self.product.name} at {self.store.name}"

    def get_absolute_url(self):
        return reverse('merchant_product_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.current_price < 0:
            raise ValidationError({'current_price': 'Current price cannot be negative.'})
        if self.original_price and self.original_price < self.current_price:
            raise ValidationError({'original_price': 'Original price must be greater than or equal to current price.'})
            
    def save(self, *args, **kwargs):
        self.clean()
        if self.original_price and self.current_price < self.original_price:
            self.discount_percentage = ((self.original_price - self.current_price) / self.original_price) * 100
        else:
            self.discount_percentage = 0.00
        super().save(*args, **kwargs)
