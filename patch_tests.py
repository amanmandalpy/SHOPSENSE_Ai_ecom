import os

def fix_tests(file_path):
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    with open(full_path, 'r') as f:
        content = f.read()
    
    # Fix imports
    content = content.replace("from products.models import Product, Brand", "from products.models import Product, Brand\nfrom categories.models import Category")
    
    # Remove bad inline imports
    content = content.replace("from categories.models import Category\n        self.category", "        self.category")
    
    with open(full_path, 'w') as f:
        f.write(content)

fix_tests('tracking/tests.py')
fix_tests('analytics/tests.py')
print("Tests fixed.")
