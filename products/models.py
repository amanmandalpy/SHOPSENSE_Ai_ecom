from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from brands.models import Brand
from categories.models import Category

class ProductStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    COMING_SOON = 'COMING_SOON', 'Coming Soon'
    DISCONTINUED = 'DISCONTINUED', 'Discontinued'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out Of Stock'

class ProductTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    # Core Data
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    
    # Relations
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Identifiers
    model_number = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Flags & Status
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.DRAFT)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    
    # Media
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    primary_image = models.ImageField(upload_to='products/primary/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    # Relationships
    tags = models.ManyToManyField(ProductTag, blank=True, related_name='products')
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')
    frequently_bought_together = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='bought_together_with')
    recommended_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='recommended_for')
    
    # Auditing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering', 'key']

    def __str__(self):
        return f"{self.key}: {self.value}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    image_title = models.CharField(max_length=255, blank=True, null=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return f"Image for {self.product.name}"
