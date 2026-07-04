from products.models import Product
from merchant_products.models import MerchantProduct
from django.utils.text import slugify

class DuplicateDetectionService:
    def __init__(self, merchant):
        self.merchant = merchant
        # Cache existing SKUs for fast lookup
        self.existing_skus = set(
            MerchantProduct.objects.filter(merchant=merchant)
            .values_list('merchant_sku', flat=True)
        )
        
        # Cache global products to find if a base product exists
        # We can map by slugified name + brand
        self.global_products = {}
        for p in Product.objects.all().select_related('brand'):
            key = f"{slugify(p.name)}-{slugify(p.brand.name) if p.brand else ''}"
            self.global_products[key] = p.id

    def is_merchant_product_duplicate(self, sku):
        """Check if merchant already has this product mapped."""
        return sku in self.existing_skus

    def find_base_product(self, name, brand_name):
        """Find an existing base product by name and brand."""
        if not name:
            return None
        key = f"{slugify(name)}-{slugify(brand_name) if brand_name else ''}"
        return self.global_products.get(key)
    
    def register_new_merchant_sku(self, sku):
        self.existing_skus.add(sku)
        
    def register_new_base_product(self, name, brand_name, product_id):
        key = f"{slugify(name)}-{slugify(brand_name) if brand_name else ''}"
        self.global_products[key] = product_id
