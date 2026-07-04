from django.contrib import admin
from .models import MerchantImportJob, MerchantSyncLog, MerchantImportError

@admin.register(MerchantImportJob)
class MerchantImportJobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'feed', 'merchant', 'status', 'started_at', 'duration_seconds', 'imported_count')
    list_filter = ('status', 'merchant')
    search_fields = ('feed__name', 'merchant__name')
    readonly_fields = ('imported_count', 'updated_count', 'skipped_count', 'failed_count', 'duration_seconds', 'started_at', 'completed_at')

@admin.register(MerchantSyncLog)
class MerchantSyncLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'merchant', 'job', 'log_level', 'message')
    list_filter = ('log_level', 'merchant')
    search_fields = ('message', 'merchant__name')

@admin.register(MerchantImportError)
class MerchantImportErrorAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'job', 'error_reason')
    list_filter = ('job__merchant',)
    search_fields = ('error_reason', 'raw_data')
