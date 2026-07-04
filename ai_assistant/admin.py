from django.contrib import admin
from .models import PromptTemplate, AILog

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'version', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'content')

@admin.register(AILog)
class AILogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'llm_provider', 'processing_time_ms', 'created_at')
    list_filter = ('llm_provider', 'created_at')
    search_fields = ('user_query', 'response_content')
    readonly_fields = ('user', 'user_query', 'llm_provider', 'prompt_used', 'response_content', 'processing_time_ms', 'created_at')
