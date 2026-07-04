from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'is_featured', 'ordering')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'ordering')
    
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'parent', 'description')}),
        ('Media', {'fields': ('icon', 'image', 'banner')}),
        ('Status', {'fields': ('is_active', 'is_featured', 'ordering')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
    )
