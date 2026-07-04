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

replace_in_file('price_tracking/services.py', [
    ('merchant_product.availability_status', 'merchant_product.stock')
])

replace_in_file('price_tracking/tests.py', [
    ('self.listing.current_price =', 'self.listing.merchant_price =')
])

print("Final patches 6 applied.")
