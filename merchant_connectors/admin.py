from django.contrib import admin
from .models import MerchantConnector, MerchantSyncLog

@admin.register(MerchantConnector)
class MerchantConnectorAdmin(admin.ModelAdmin):
    list_display = ('store', 'api_url', 'is_active', 'last_sync_time')
    list_filter = ('is_active',)

@admin.register(MerchantSyncLog)
class MerchantSyncLogAdmin(admin.ModelAdmin):
    list_display = ('connector', 'sync_type', 'status', 'records_processed', 'start_time')
    list_filter = ('status', 'sync_type', 'start_time')
    search_fields = ('connector__store__name',)
