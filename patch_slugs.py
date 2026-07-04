import os
import re

files_to_fix = [
    'merchant_products/tests.py',
    'ai_assistant/tests.py',
    'search/tests.py',
    'offers/tests.py',
    'price_tracking/tests.py',
    'price_alerts/tests.py'
]

for file_path in files_to_fix:
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    if not os.path.exists(full_path):
        continue
        
    with open(full_path, 'r') as f:
        content = f.read()
        
    # Remove slug='...' from Merchant.objects.create(...)
    content = re.sub(r",\s*slug='[^']*'", "", content)
    
    with open(full_path, 'w') as f:
        f.write(content)

print("Slugs removed.")
