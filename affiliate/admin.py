from django.contrib import admin
from .models import AffiliateConfig, AffiliateClick

@admin.register(AffiliateConfig)
class AffiliateConfigAdmin(admin.ModelAdmin):
    list_display = ('store', 'affiliate_id', 'tracking_param_name', 'is_active')
    list_filter = ('is_active',)

@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ('merchant_product', 'user', 'click_time', 'ip_address')
    list_filter = ('click_time',)
    search_fields = ('merchant_product__product__name', 'outbound_url')
