from django.contrib import admin
from .models import SearchQuery

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'search_count', 'last_results_count', 'last_searched_at')
    list_filter = ('last_searched_at',)
    search_fields = ('keyword',)
    readonly_fields = ('keyword', 'search_count', 'last_results_count', 'last_searched_at')
