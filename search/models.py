from django.db import models
from django.utils import timezone

class SearchQuery(models.Model):
    keyword = models.CharField(max_length=255, unique=True, db_index=True)
    search_count = models.PositiveIntegerField(default=1)
    last_results_count = models.PositiveIntegerField(default=0)
    last_searched_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-search_count', '-last_searched_at']
        verbose_name_plural = "Search Queries"

    def __str__(self):
        return f"{self.keyword} ({self.search_count})"
