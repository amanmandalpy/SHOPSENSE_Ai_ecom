from django.contrib import admin
from .models import LegalDocument

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'last_updated')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
