from django.db import models

class UrlRedirect(models.Model):
    old_path = models.CharField(max_length=255, unique=True, help_text="e.g. /old-product/")
    new_path = models.CharField(max_length=255, help_text="e.g. /products/new-product/")
    is_permanent = models.BooleanField(default=True, help_text="Use 301 for permanent, 302 for temporary")
    
    def __str__(self):
        return f"{self.old_path} -> {self.new_path}"

class GlobalMeta(models.Model):
    site_name = models.CharField(max_length=100, default='ShopSense AI')
    default_title = models.CharField(max_length=200)
    default_description = models.TextField()
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.site_name
