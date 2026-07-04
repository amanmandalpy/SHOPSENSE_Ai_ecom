from django.contrib import admin
from django.utils.html import format_html
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'slug', 'country', 'rating', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'country')
    search_fields = ('name', 'description', 'website_url')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured')
    
    fieldsets = (
        ('Identity', {'fields': ('name', 'slug', 'description', 'logo', 'banner')}),
        ('Links', {'fields': ('website_url', 'affiliate_base_url', 'support_contact')}),
        ('Metadata', {'fields': ('country', 'currency', 'rating', 'color_theme')}),
        ('Status', {'fields': ('is_active', 'is_featured')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 40px; border-radius: 4px;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'
