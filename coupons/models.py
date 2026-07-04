from django.db import models
from django.utils import timezone
from affiliate.models import Merchant

class DiscountType(models.TextChoices):
    FLAT = 'FLAT', 'Flat Discount'
    PERCENTAGE = 'PERCENTAGE', 'Percentage Discount'

class CouponStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    EXPIRED = 'EXPIRED', 'Expired'
    DISABLED = 'DISABLED', 'Disabled'

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True)
    
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum absolute discount for percentage coupons")
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    
    status = models.CharField(max_length=20, choices=CouponStatus.choices, default=CouponStatus.ACTIVE)
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    per_user_limit = models.PositiveIntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-valid_until']

    def __str__(self):
        return self.code
        
    def is_valid(self):
        now = timezone.now()
        if self.status != CouponStatus.ACTIVE:
            return False
        if not (self.valid_from <= now <= self.valid_until):
            return False
        return True
