from django.db import models
from django.conf import settings
from products.models import Product

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('SCHEDULED', 'Scheduled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(BlogTag, blank=True)
    related_products = models.ManyToManyField(Product, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    reading_time = models.IntegerField(default=5, help_text="Reading time in minutes")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to='blog/og/', null=True, blank=True)
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
