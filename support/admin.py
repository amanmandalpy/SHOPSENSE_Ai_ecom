from django.contrib import admin
from .models import FAQCategory, FAQ, SupportTicket

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_published', 'order')
    list_filter = ('category', 'is_published')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'ticket_type', 'email', 'status', 'created_at')
    list_filter = ('status', 'ticket_type', 'created_at')
    search_fields = ('subject', 'email', 'message')
