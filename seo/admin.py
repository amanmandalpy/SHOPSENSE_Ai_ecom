from django.contrib import admin
from .models import UrlRedirect, GlobalMeta

@admin.register(UrlRedirect)
class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'is_permanent')
    list_filter = ('is_permanent',)
    search_fields = ('old_path', 'new_path')

@admin.register(GlobalMeta)
class GlobalMetaAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'default_title')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
