from django.contrib import admin
from .models import MerchantProduct

@admin.register(MerchantProduct)
class MerchantProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'merchant', 'merchant_price', 'stock', 'last_updated')
    list_filter = ('merchant', 'stock')
    search_fields = ('product__name', 'merchant__name', 'merchant_sku')
    autocomplete_fields = ('product', 'merchant')
    
    fieldsets = (
        ('Mapping Identity', {
            'fields': ('product', 'merchant', 'merchant_sku')
        }),
        ('URLs', {
            'fields': ('merchant_product_url', 'affiliate_url')
        }),
        ('Pricing & Status', {
            'fields': ('merchant_price', 'original_price', 'stock', 'seller', 'rating', 'delivery_charge')
        }),
    )
