from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'store', 'discount_type', 'discount_value', 'status', 'valid_until')
    list_filter = ('status', 'discount_type', 'store')
    search_fields = ('code', 'name')
