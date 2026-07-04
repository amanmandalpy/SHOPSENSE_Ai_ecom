import os
import json

def replace_in_file(file_path, replacements):
    full_path = os.path.join(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce', file_path)
    with open(full_path, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(full_path, 'w') as f:
        f.write(content)

replace_in_file('tracking/tests.py', [
    ("is_active=True", "status='ACTIVE'")
])

with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\analytics\services.py', 'r') as f:
    content = f.read()

# Fix dict parsing for JSONField in SQLite test env
content = content.replace("pid = str(v.metadata.get('product_id', ''))", 
"""
            import json
            meta = v.metadata
            if isinstance(meta, str):
                try: meta = json.loads(meta)
                except: meta = {}
            pid = str(meta.get('product_id', ''))
""")

with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\analytics\services.py', 'w') as f:
    f.write(content)

print("Patched 2.")
