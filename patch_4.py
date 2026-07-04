import os

def replace_in_file(file_path, replacements):
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    if not os.path.exists(full_path):
        return
    with open(full_path, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(full_path, 'w') as f:
        f.write(content)

# Fix seller_rating
replace_in_file('price_tracking/services.py', [
    ('seller_rating_snapshot=merchant_product.seller_rating,', 'seller_rating_snapshot=merchant_product.rating,')
])

# Fix get_absolute_url property or method call
replace_in_file('price_alerts/tasks.py', [
    ('alert.merchant_product.get_absolute_url()', 'alert.merchant_product.get_absolute_url')
])

# Also fix the definition in models to be a property just in case
replace_in_file('merchant_products/models.py', [
    ('def get_absolute_url(self):\n        return self.product.get_absolute_url()', '@property\n    def get_absolute_url(self):\n        return getattr(self.product, "get_absolute_url", f"/product/{self.product.slug}/")')
])

print("Final patches 4 applied.")
