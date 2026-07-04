from django.contrib import admin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'country', 'founded_year', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'country')
    search_fields = ('name', 'description', 'country')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured')
    
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'website', 'country', 'founded_year')}),
        ('Media', {'fields': ('logo', 'banner')}),
        ('Status', {'fields': ('is_active', 'is_featured')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
        ('Social', {'fields': ('facebook_url', 'twitter_url', 'instagram_url')}),
    )
