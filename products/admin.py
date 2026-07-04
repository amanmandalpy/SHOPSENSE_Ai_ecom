from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductTag, ProductSpecification, ProductImage

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'name', 'brand', 'category', 'sku', 'status', 'is_featured')
    list_filter = ('status', 'brand', 'category', 'is_featured', 'is_trending', 'is_new_arrival')
    search_fields = ('name', 'sku', 'barcode', 'model_number')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('status', 'is_featured')
    inlines = [ProductSpecificationInline, ProductImageInline]
    filter_horizontal = ('tags', 'related_products', 'frequently_bought_together', 'recommended_products')
    
    fieldsets = (
        ('Core Information', {
            'fields': ('name', 'slug', 'short_description', 'full_description', 'brand', 'category')
        }),
        ('Identifiers', {
            'fields': ('model_number', 'sku', 'barcode')
        }),
        ('Media', {
            'fields': ('thumbnail', 'primary_image')
        }),
        ('Status & Flags', {
            'fields': ('status', 'is_featured', 'is_trending', 'is_new_arrival', 'is_best_seller')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Relationships', {
            'fields': ('tags', 'related_products', 'frequently_bought_together', 'recommended_products')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height: 40px; border-radius: 4px;" />', obj.thumbnail.url)
        return "-"
    thumbnail_preview.short_description = 'Image'
