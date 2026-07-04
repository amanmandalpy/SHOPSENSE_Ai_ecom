import os

CORE_DIR = 'd:\\PYTHON_PROJECTS\\SHOPSENSE_Ai_ecommerce\\templates\\core'
os.makedirs(CORE_DIR, exist_ok=True)

trust_pages = ['about', 'mission', 'how-it-works', 'why-trust-us']

base_template = """{% extends 'base.html' %}
{% block title %}{title} - ShopSense AI{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
    <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">{title}</h1>
    <p class="text-lg text-gray-600 dark:text-gray-400 mb-12">Learn more about our platform and why millions of shoppers trust ShopSense AI.</p>
    
    <div class="prose prose-lg prose-blue dark:prose-invert max-w-none text-left bg-white dark:bg-gray-800 p-8 md:p-12 rounded-3xl border border-gray-100 dark:border-gray-700 shadow-sm">
        <p>This is a placeholder for the <strong>{title}</strong> page. In a production environment, this content would highlight the specific details of ShopSense AI's operations, technology, and team.</p>
        <p>Our goal is to create the most transparent, AI-driven shopping experience on the internet.</p>
    </div>
</div>
{% endblock %}
"""

for page in trust_pages:
    title = page.replace('-', ' ').title()
    content = base_template.replace('{title}', title)
    with open(os.path.join(CORE_DIR, f"{page}.html"), 'w') as f:
        f.write(content)

print("Trust pages generated.")
