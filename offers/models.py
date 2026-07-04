from django.db import models
from django.utils import timezone
from affiliate.models import Merchant

class OfferType(models.TextChoices):
    BANK_DISCOUNT = 'BANK_DISCOUNT', 'Bank Discount'
    CASHBACK = 'CASHBACK', 'Cashback'
    NO_COST_EMI = 'NO_COST_EMI', 'No Cost EMI'
    FESTIVAL = 'FESTIVAL', 'Festival Offer'

class DiscountType(models.TextChoices):
    FLAT = 'FLAT', 'Flat'
    PERCENTAGE = 'PERCENTAGE', 'Percentage'

class BankOffer(models.Model):
    name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=100) # e.g. HDFC, ICICI, SBI
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='bank_offers', null=True, blank=True)
    
    offer_type = models.CharField(max_length=50, choices=OfferType.choices, default=OfferType.BANK_DISCOUNT)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    terms_and_conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bank_name} - {self.name}"

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        return self.valid_from <= now <= self.valid_until
