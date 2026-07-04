import os
import re

# Fix redirect_service.py
path1 = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', 'affiliate/services/redirect_service.py')
with open(path1, 'r') as f: content = f.read()
content = content.replace(
    "user=request.user if request.user.is_authenticated else None",
    "user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None"
)
with open(path1, 'w') as f: f.write(content)

# Fix affiliate/views.py
path2 = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', 'affiliate/views.py')
with open(path2, 'r') as f: content = f.read()
content = content.replace(
    "if not merchant_product.merchant.is_active:",
    "if merchant_product.merchant.status != 'ACTIVE':"
)
with open(path2, 'w') as f: f.write(content)

# Fix analytics/services.py (clean ctr calculation)
path3 = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', 'analytics/services.py')
with open(path3, 'r') as f: content = f.read()
new_ctr = """    @staticmethod
    def calculate_product_ctrs():
        views = PlatformEvent.objects.filter(event_type=EventType.PRODUCT_VIEW)
        views_dict = {}
        for v in views:
            meta = v.metadata
            if isinstance(meta, str):
                import json
                try: meta = json.loads(meta.replace("'", '"'))
                except: meta = {}
            if not isinstance(meta, dict):
                meta = {}
            pid = str(meta.get('product_id', ''))
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
content = re.sub(r'    @staticmethod\n    def calculate_product_ctrs\(.*', new_ctr, content, flags=re.DOTALL)
with open(path3, 'w') as f: f.write(content)

print("Patched 3.")
