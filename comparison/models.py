from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from products.models import Product

class ComparisonList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comparison_list', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Comparison List for {self.user.username}"
        return f"Comparison List (Session: {self.session_key})"

class ComparisonItem(models.Model):
    comparison_list = models.ForeignKey(ComparisonList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='compare_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comparison_list', 'product')
        ordering = ['added_at']

    def __str__(self):
        return f"{self.product.name} in {self.comparison_list}"

    def clean(self):
        if self.product.status != 'ACTIVE':
            raise ValidationError("Cannot compare inactive products.")
        
        if self.comparison_list_id:
            if ComparisonItem.objects.filter(comparison_list_id=self.comparison_list_id).exclude(pk=self.pk).count() >= 4:
                raise ValidationError("You can only compare a maximum of 4 products.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
