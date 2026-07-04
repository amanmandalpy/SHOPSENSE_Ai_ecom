from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Min, Max
from .models import ComparisonList, ComparisonItem
from products.models import Product

def get_or_create_comparison_list(request):
    """Retrieves or creates a comparison list based on User or Session."""
    if request.user.is_authenticated:
        comp_list, _ = ComparisonList.objects.get_or_create(user=request.user)
        return comp_list
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        comp_list, _ = ComparisonList.objects.get_or_create(session_key=session_key)
        return comp_list

def add_product_to_compare(request, product_id):
    """Adds a product to the comparison list, enforcing the 4-item limit."""
    product = Product.objects.filter(id=product_id, status='ACTIVE').first()
    if not product:
        raise ValueError("Product not found or inactive.")
        
    comp_list = get_or_create_comparison_list(request)
    
    if comp_list.items.count() >= 4:
        raise ValueError("You can only compare up to 4 products at a time.")
        
    if comp_list.items.filter(product=product).exists():
        raise ValueError("This product is already in your comparison list.")
        
    ComparisonItem.objects.create(comparison_list=comp_list, product=product)

def remove_product_from_compare(request, product_id):
    """Removes a product from the comparison list."""
    comp_list = get_or_create_comparison_list(request)
    comp_list.items.filter(product_id=product_id).delete()

def clear_comparison_list(request):
    comp_list = get_or_create_comparison_list(request)
    comp_list.items.all().delete()

def get_dynamic_comparison_matrix(comp_list):
    """
    Parses the items in the list and builds a dynamic, tabular-ready matrix.
    Extracts all unique specification keys across all products.
    """
    items = comp_list.items.select_related('product', 'product__brand', 'product__category').prefetch_related(
        'product__specifications', 'product__merchant_listings', 'product__merchant_listings__store', 'product__gallery_images'
    ).all()
    
    products = [item.product for item in items]
    if not products:
        return {'products': [], 'specifications': {}, 'highlights': {}}
        
    # Gather all unique spec keys
    all_spec_keys = set()
    for product in products:
        for spec in product.specifications.all():
            all_spec_keys.add(spec.key)
            
    # Sort spec keys alphabetically for consistent rendering
    sorted_spec_keys = sorted(list(all_spec_keys))
    
    # Build spec matrix: { "RAM": ["8GB", "16GB", "N/A", "N/A"] }
    spec_matrix = {key: [] for key in sorted_spec_keys}
    
    # Calculate highlights
    prices = []
    
    for product in products:
        prod_specs = {s.key: s.value for s in product.specifications.all()}
        for key in sorted_spec_keys:
            spec_matrix[key].append(prod_specs.get(key, "-"))
            
        # Price tracking for highlights
        best_listing = product.merchant_listings.order_by('current_price').first()
        if best_listing:
            prices.append(best_listing.current_price)
            
    highlights = {}
    if prices:
        highlights['lowest_price'] = min(prices)
        highlights['highest_price'] = max(prices)
        
    return {
        'products': products,
        'specifications': spec_matrix,
        'highlights': highlights
    }
