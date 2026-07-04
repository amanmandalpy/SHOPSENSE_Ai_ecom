from django.contrib import admin
from .models import Merchant, AffiliateAccount

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'affiliate_supported', 'priority', 'last_sync')
    list_filter = ('status', 'affiliate_supported', 'official_api_supported')
    search_fields = ('name', 'website')
    ordering = ('-priority', 'name')

@admin.register(AffiliateAccount)
class AffiliateAccountAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'affiliate_id', 'commission_status')
    list_filter = ('commission_status',)
    search_fields = ('merchant__name', 'affiliate_id')
