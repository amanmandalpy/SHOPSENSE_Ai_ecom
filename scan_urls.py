import os, re
from django.urls import NoReverseMatch, reverse

template_dir = r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\templates'
url_pattern = re.compile(r"""\{%-?\s*url\s+['"]([^'"]+)['"](?:\s+[^%]+)?\s*-?%\}""")

broken = []
all_found = []
for root, dirs, files in os.walk(template_dir):
    for fname in files:
        if not fname.endswith('.html'): continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in url_pattern.finditer(content):
            name = m.group(1)
            all_found.append(name)
            is_ok = False
            for attempt in [
                lambda: reverse(name),
                lambda: reverse(name, args=[1]),
                lambda: reverse(name, args=['test']),
                lambda: reverse(name, kwargs={'slug': 'test'}),
                lambda: reverse(name, kwargs={'pk': 1}),
                lambda: reverse(name, kwargs={'token': '00000000-0000-0000-0000-000000000000'}),
            ]:
                try:
                    attempt()
                    is_ok = True
                    break
                except (NoReverseMatch, Exception):
                    pass
            if not is_ok:
                relpath = fpath.replace(template_dir, '')
                broken.append((relpath, name))

print(f'Scanned {len(set(all_found))} unique URL names')
print(f'Found {len(set(broken))} broken url tags:')
for f, n in sorted(set(broken)):
    print(f'  {f}: [{n}]')
