from django.contrib import admin
from .models import PriceHistory

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('merchant_product', 'price', 'recorded_at', 'availability_status')
    list_filter = ('recorded_at', 'merchant_product__merchant', 'availability_status')
    search_fields = ('merchant_product__product__name', 'merchant_product__merchant__name')
    date_hierarchy = 'recorded_at'
    readonly_fields = [f.name for f in PriceHistory._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
