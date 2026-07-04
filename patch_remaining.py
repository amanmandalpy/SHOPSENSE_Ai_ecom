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

# coupons and offers models & admin
replace_in_file('coupons/models.py', [
    ('from stores.models import Store', 'from affiliate.models import Merchant'),
    ('store = models.ForeignKey(Store,', "merchant = models.ForeignKey(Merchant,"),
])
replace_in_file('offers/models.py', [
    ('from stores.models import Store', 'from affiliate.models import Merchant'),
    ('store = models.ForeignKey(Store,', "merchant = models.ForeignKey(Merchant,"),
])
replace_in_file('coupons/admin.py', [('store', 'merchant')])
replace_in_file('offers/admin.py', [('store', 'merchant')])

# fix comparison services
replace_in_file('comparison/services.py', [
    ("order_by('current_price')", "order_by('merchant_price')")
])

# fix price alerts tests
replace_in_file('price_alerts/tests.py', [
    ('self.listing.current_price =', 'self.listing.merchant_price =')
])

print("Fixes applied.")
