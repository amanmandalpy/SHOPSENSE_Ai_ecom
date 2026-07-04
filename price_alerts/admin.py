from django.contrib import admin
from .models import PriceAlert

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'merchant_product', 'target_price', 'status', 'alert_type', 'notification_sent')
    list_filter = ('status', 'alert_type', 'notification_sent', 'created_at')
    search_fields = ('user__username', 'merchant_product__product__name')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at', 'triggered_at')
