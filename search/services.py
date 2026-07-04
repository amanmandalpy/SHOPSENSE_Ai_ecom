import re
from django.db.models import Q, Min, Max
from products.models import Product
from .models import SearchQuery
from django.utils import timezone

def clean_keyword(keyword):
    """Trims spaces, ignores multiple spaces."""
    if not keyword:
        return ""
    keyword = str(keyword).strip()
    return re.sub(r'\s+', ' ', keyword)

def log_search(keyword, results_count):
    if not keyword:
        return
    keyword = clean_keyword(keyword).lower()
    obj, created = SearchQuery.objects.get_or_create(keyword=keyword)
    if not created:
        obj.search_count += 1
    obj.last_results_count = results_count
    obj.last_searched_at = timezone.now()
    obj.save()

def execute_search(query_string, filters=None, sort_by=None):
    if filters is None:
        filters = {}
        
    query_string = clean_keyword(query_string)
    
    # Base queryset for active products
    qs = Product.objects.filter(status='ACTIVE')
    
    # Main search keyword logic
    if query_string:
        qs = qs.filter(
            Q(name__icontains=query_string) |
            Q(brand__name__icontains=query_string) |
            Q(category__name__icontains=query_string) |
            Q(sku__icontains=query_string) |
            Q(tags__name__icontains=query_string) |
            Q(short_description__icontains=query_string) |
            Q(merchant_listings__store__name__icontains=query_string)
        ).distinct()
        
    # Filtering logic
    if 'category' in filters and filters['category']:
        qs = qs.filter(category__slug=filters['category'])
        
    if 'brand' in filters and filters['brand']:
        qs = qs.filter(brand__slug=filters['brand'])
        
    if 'store' in filters and filters['store']:
        qs = qs.filter(merchant_listings__store__slug=filters['store']).distinct()
        
    if 'min_price' in filters and filters['min_price']:
        qs = qs.filter(merchant_listings__current_price__gte=filters['min_price']).distinct()
        
    if 'max_price' in filters and filters['max_price']:
        qs = qs.filter(merchant_listings__current_price__lte=filters['max_price']).distinct()
        
    # Optimizations
    qs = qs.select_related('brand', 'category')
    qs = qs.prefetch_related('merchant_listings', 'merchant_listings__store', 'gallery_images')
    
    # Sorting logic
    if sort_by:
        if sort_by == 'lowest_price':
            qs = qs.annotate(min_price=Min('merchant_listings__current_price')).order_by('min_price')
        elif sort_by == 'highest_price':
            qs = qs.annotate(max_price=Max('merchant_listings__current_price')).order_by('-max_price')
        elif sort_by == 'highest_discount':
            qs = qs.annotate(max_discount=Max('merchant_listings__discount_percentage')).order_by('-max_discount')
        elif sort_by == 'newest':
            qs = qs.order_by('-created_at')
        elif sort_by == 'a_z':
            qs = qs.order_by('name')
        elif sort_by == 'z_a':
            qs = qs.order_by('-name')
            
    # Important: if using annotations with distinct, fields must match. 
    # For now, distinct() on base qs is sufficient unless sorted.
    return qs.distinct() if not sort_by else qs
