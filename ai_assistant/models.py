from django.db import models
from django.conf import settings

class PromptCategory(models.TextChoices):
    RECOMMENDATION = 'RECOMMENDATION', 'Recommendation'
    COMPARISON = 'COMPARISON', 'Comparison'
    BUYING_GUIDE = 'BUYING_GUIDE', 'Buying Guide'
    GENERAL_ADVICE = 'GENERAL_ADVICE', 'General Advice'

class PromptTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=PromptCategory.choices)
    content = models.TextField(help_text="Use {{ variables }} for dynamic injection.")
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (v{self.version})"

class AILog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    user_query = models.TextField()
    llm_provider = models.CharField(max_length=50)
    prompt_used = models.TextField()
    response_content = models.TextField()
    processing_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query from {self.user} via {self.llm_provider}"
