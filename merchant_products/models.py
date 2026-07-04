from django.db import models
from products.models import Product
from affiliate.models import Merchant

class StockStatus(models.TextChoices):
    IN_STOCK = 'IN_STOCK', 'In Stock'
    LIMITED_STOCK = 'LIMITED_STOCK', 'Limited Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out Of Stock'
    COMING_SOON = 'COMING_SOON', 'Coming Soon'
    DISCONTINUED = 'DISCONTINUED', 'Discontinued'

class MerchantProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='merchant_listings')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='merchant_products', null=True, blank=True)
    
    # URLs
    merchant_product_url = models.URLField(max_length=1000)
    merchant_sku = models.CharField(max_length=100, blank=True, null=True)
    affiliate_url = models.URLField(max_length=1000, blank=True, null=True)
    
    # Pricing
    merchant_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Info
    stock = models.CharField(max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK)
    seller = models.CharField(max_length=200, blank=True, help_text="Specific third-party seller on the merchant platform")
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Sync status
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'merchant')
        ordering = ['merchant_price']

    def __str__(self):
        return f"{self.merchant.name} - {self.product.name}"
        
    def clean(self):
        if self.merchant_price and self.merchant_price < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({'merchant_price': 'Price cannot be negative.'})
        if self.original_price and self.original_price < self.merchant_price:
            from django.core.exceptions import ValidationError
            raise ValidationError({'original_price': 'Original price cannot be less than current price.'})
    
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.merchant_price:
            return ((self.original_price - self.merchant_price) / self.original_price) * 100
        return 0.00
        
    # Backwards compatibility properties to avoid completely breaking the frontend
    @property
    def get_absolute_url(self):
        return self.product.get_absolute_url()

    @property
    def current_price(self):
        return self.merchant_price
        
    @property
    def store(self):
        return self.merchant
