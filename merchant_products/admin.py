from django.contrib import admin
from .models import MerchantProduct

@admin.register(MerchantProduct)
class MerchantProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'current_price', 'discount_percentage', 'availability_status', 'last_synced', 'is_active')
    list_filter = ('store', 'availability_status', 'is_active')
    search_fields = ('product__name', 'store__name', 'merchant_sku', 'seller_name')
    list_editable = ('is_active', 'availability_status')
    autocomplete_fields = ('product', 'store')
    
    fieldsets = (
        ('Mapping Identity', {
            'fields': ('product', 'store', 'merchant_sku')
        }),
        ('URLs', {
            'fields': ('merchant_product_url', 'affiliate_url')
        }),
        ('Pricing', {
            'fields': ('current_price', 'original_price', 'currency')
        }),
        ('Logistics & Seller', {
            'fields': ('availability_status', 'delivery_charge', 'estimated_delivery_days', 'seller_name', 'seller_rating')
        }),
        ('Features', {
            'fields': ('cashback_available', 'emi_available', 'cod_available', 'exchange_available', 'warranty')
        }),
        ('Audit', {
            'fields': ('last_synced', 'is_active')
        }),
    )
    readonly_fields = ('discount_percentage',)
