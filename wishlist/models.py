from django.db import models
from django.conf import settings
from products.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    name = models.CharField(max_length=100, default='My Wishlist')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user}'s {self.name}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.name}"
