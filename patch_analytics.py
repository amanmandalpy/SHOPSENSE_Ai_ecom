import os

def replace_in_file(file_path, replacements):
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    with open(full_path, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(full_path, 'w') as f:
        f.write(content)

replace_in_file('tracking/tests.py', [
    ("slug='amazon', is_active=True", "status='ACTIVE'"),
    ("slug='apple'", "")
])

# Rewrite calculate_product_ctrs in analytics/services.py
new_ctr = """    @staticmethod
    def calculate_product_ctrs():
        views = PlatformEvent.objects.filter(event_type=EventType.PRODUCT_VIEW)
        views_dict = {}
        for v in views:
            pid = str(v.metadata.get('product_id', ''))
            if pid.isdigit():
                views_dict[pid] = views_dict.get(pid, 0) + 1
                
        clicks = AffiliateClick.objects.values('product_id').annotate(count=Count('id'))
        clicks_dict = {str(item['product_id']): item['count'] for item in clicks if item['product_id']}
        
        all_product_ids = set(list(views_dict.keys()) + list(clicks_dict.keys()))
        
        for pid in all_product_ids:
            if not pid.isdigit(): continue
            view_count = views_dict.get(pid, 0)
            click_count = clicks_dict.get(pid, 0)
            
            pa, _ = ProductAnalytics.objects.get_or_create(product_id=int(pid))
            pa.views_count = view_count
            pa.affiliate_clicks = click_count
            pa.calculate_ctr()
"""

with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\analytics\services.py', 'r') as f:
    content = f.read()
    
# Replace everything after calculate_product_ctrs
import re
content = re.sub(r'    @staticmethod\n    def calculate_product_ctrs\(.*', new_ctr, content, flags=re.DOTALL)

with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\analytics\services.py', 'w') as f:
    f.write(content)

print("Patched.")
