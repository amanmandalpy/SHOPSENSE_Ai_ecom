from django.contrib import admin
from .models import PlatformEvent, MerchantAnalytics, ProductAnalytics, CampaignAnalytics

@admin.register(PlatformEvent)
class PlatformEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'session_key', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('session_key',)
    readonly_fields = ('event_type', 'user', 'session_key', 'metadata', 'created_at')

@admin.register(MerchantAnalytics)
class MerchantAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'date', 'total_clicks', 'unique_clicks')
    list_filter = ('merchant', 'date')
    search_fields = ('merchant__name',)

@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('product', 'views_count', 'affiliate_clicks', 'ctr', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('product__name',)

@admin.register(CampaignAnalytics)
class CampaignAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'date', 'total_clicks', 'unique_clicks')
    list_filter = ('campaign', 'date')
    search_fields = ('campaign__name', 'campaign__code')
