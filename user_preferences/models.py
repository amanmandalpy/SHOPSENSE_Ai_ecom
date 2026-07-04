from django.db import models
from django.conf import settings
from categories.models import Category
from brands.models import Brand
from products.models import Product
from stores.models import Store

class UserPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    preferred_categories = models.ManyToManyField(Category, blank=True)
    preferred_brands = models.ManyToManyField(Brand, blank=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_currency = models.CharField(max_length=10, default='USD')
    
    def __str__(self):
        return f"{self.user}'s Preferences"

class BrowsingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='browsing_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True) # Updates automatically on subsequent views
    
    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'product') # One row per product per user

    def __str__(self):
        return f"{self.user} viewed {self.product.name}"

class SavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    query = models.CharField(max_length=255)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        unique_together = ('user', 'query')
