import os
import re

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

# Fix cashback_available
replace_in_file('price_tracking/services.py', [
    ('cashback_snapshot=merchant_product.cashback_available', 'cashback_snapshot=False')
])

# Restore get_absolute_url to be a normal method and use ()
replace_in_file('merchant_products/models.py', [
    ('@property\n    def get_absolute_url(self):\n        return getattr(self.product, "get_absolute_url", f"/product/{self.product.slug}/")', 'def get_absolute_url(self):\n        return self.product.get_absolute_url()')
])

replace_in_file('price_alerts/tasks.py', [
    ('action_url=alert.merchant_product.get_absolute_url,', 'action_url=alert.merchant_product.get_absolute_url(),')
])

print("Final patches 5 applied.")
