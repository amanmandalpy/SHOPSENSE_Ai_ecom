from django.contrib import admin
from .models import AffiliateClick, ClickSession, Campaign, UTMSource

@admin.register(UTMSource)
class UTMSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'source', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'source')
    search_fields = ('name', 'code')

@admin.register(ClickSession)
class ClickSessionAdmin(admin.ModelAdmin):
    list_display = ('session_identifier', 'pages_viewed', 'clicks_count', 'session_duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session_identifier', 'visitor_identifier')
    readonly_fields = ('session_identifier', 'visitor_identifier', 'entry_page', 'exit_page', 'pages_viewed', 'session_duration', 'clicks_count', 'created_at', 'updated_at')

@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'merchant', 'product', 'user', 'utm_source', 'click_timestamp')
    list_filter = ('merchant', 'utm_source', 'click_timestamp', 'device_type')
    search_fields = ('affiliate_url', 'original_merchant_url', 'ip_address')
    readonly_fields = ('user', 'session', 'merchant', 'merchant_product', 'product', 'affiliate_url', 'original_merchant_url', 'utm_source', 'utm_medium', 'utm_campaign', 'campaign', 'ip_address', 'country', 'region', 'city', 'device_type', 'operating_system', 'browser', 'referrer', 'click_timestamp')
