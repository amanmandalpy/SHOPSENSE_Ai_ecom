from django.contrib import admin
from .models import ComparisonList, ComparisonItem

class ComparisonItemInline(admin.TabularInline):
    model = ComparisonItem
    extra = 0
    max_num = 4

@admin.register(ComparisonList)
class ComparisonListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'updated_at')
    inlines = [ComparisonItemInline]
    search_fields = ('user__username', 'session_key')
