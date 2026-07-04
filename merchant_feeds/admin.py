from django.contrib import admin
from .models import MerchantFeed, MerchantFeedHistory

@admin.register(MerchantFeed)
class MerchantFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'feed_type', 'status', 'last_sync', 'next_sync', 'total_products')
    list_filter = ('status', 'feed_type', 'merchant')
    search_fields = ('name', 'merchant__name')
    actions = ['pause_feeds', 'resume_feeds']
    
    def pause_feeds(self, request, queryset):
        queryset.update(status='PAUSED')
    pause_feeds.short_description = "Pause selected feeds"
    
    def resume_feeds(self, request, queryset):
        queryset.update(status='ACTIVE')
    resume_feeds.short_description = "Resume selected feeds"

@admin.register(MerchantFeedHistory)
class MerchantFeedHistoryAdmin(admin.ModelAdmin):
    list_display = ('feed', 'timestamp', 'status', 'total_products')
    list_filter = ('status', 'feed__merchant')
    search_fields = ('feed__name',)
