from django.contrib import admin
from .models import NewsletterSubscription, ContactMessage

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
