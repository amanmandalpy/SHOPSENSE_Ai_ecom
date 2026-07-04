from django.contrib import admin
from .models import BankOffer

@admin.register(BankOffer)
class BankOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_name', 'store', 'offer_type', 'discount_value', 'is_active')
    list_filter = ('is_active', 'offer_type', 'bank_name', 'store')
    search_fields = ('name', 'bank_name')
