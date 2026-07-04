from django.contrib import admin
from .models import SiteSettings, SystemLog, HomepageBanner

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('module', 'level', 'user', 'ip_address', 'created_at')
    list_filter = ('level', 'module', 'created_at')
    search_fields = ('message', 'module')
    readonly_fields = ('level', 'module', 'message', 'user', 'ip_address', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
