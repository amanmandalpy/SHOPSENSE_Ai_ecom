import os

SUPPORT_DIR = 'd:\\PYTHON_PROJECTS\\SHOPSENSE_Ai_ecommerce\\templates\\support'
LEGAL_DIR = 'd:\\PYTHON_PROJECTS\\SHOPSENSE_Ai_ecommerce\\templates\\legal'
os.makedirs(SUPPORT_DIR, exist_ok=True)
os.makedirs(LEGAL_DIR, exist_ok=True)

help_center_html = """{% extends 'base.html' %}
{% block title %}Help Center - ShopSense AI{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="text-center mb-16">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-6">How can we help you?</h1>
        <form method="get" action="{% url 'support_home' %}" class="max-w-2xl mx-auto relative">
            <i class="fa-solid fa-search absolute left-5 top-1/2 -translate-y-1/2 text-gray-400"></i>
            <input type="text" name="q" value="{{ request.GET.q }}" placeholder="Search for articles, guides, and FAQs..." class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full py-4 pl-12 pr-6 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none shadow-sm transition">
        </form>
    </div>

    {% if search_results is not None %}
        <div class="max-w-4xl mx-auto">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Search Results</h2>
            {% if search_results %}
                <div class="space-y-4">
                    {% for faq in search_results %}
                    <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">{{ faq.question }}</h3>
                        <p class="text-gray-600 dark:text-gray-400">{{ faq.answer }}</p>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-gray-500 dark:text-gray-400 text-center py-12">No results found for "{{ request.GET.q }}".</p>
            {% endif %}
        </div>
    {% else %}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for category in categories %}
            <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-lg transition group">
                <div class="w-14 h-14 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center text-primary text-2xl mb-6 group-hover:scale-110 transition">
                    <i class="{{ category.icon|default:'fa-solid fa-book' }}"></i>
                </div>
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">{{ category.name }}</h3>
                <ul class="space-y-3">
                    {% for faq in category.faqs.all|slice:":3" %}
                    <li>
                        <a href="?q={{ faq.question|urlencode }}" class="text-gray-600 hover:text-primary dark:text-gray-400 dark:hover:text-primary transition flex items-start gap-2">
                            <i class="fa-solid fa-file-lines mt-1 text-xs"></i> {{ faq.question }}
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                {% if category.faqs.count > 3 %}
                <a href="#" class="inline-block mt-6 text-sm font-semibold text-primary hover:text-blue-600 transition">View all {{ category.faqs.count }} articles <i class="fa-solid fa-arrow-right ml-1"></i></a>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    {% endif %}

    <div class="mt-20 bg-primary rounded-3xl p-12 text-center text-white relative overflow-hidden">
        <div class="relative z-10">
            <h2 class="text-3xl font-bold mb-4">Still need help?</h2>
            <p class="text-blue-100 mb-8 max-w-xl mx-auto">Our support team is always ready to help you with any issues or questions you might have.</p>
            <a href="{% url 'support_contact' %}" class="inline-block bg-white text-primary font-semibold py-4 px-8 rounded-full hover:bg-gray-50 transition shadow-lg hover-lift">Contact Support</a>
        </div>
        <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 opacity-50"></div>
    </div>
</div>
{% endblock %}
"""

contact_html = """{% extends 'base.html' %}
{% block title %}Contact Support - ShopSense AI{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="text-center mb-12">
        <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">Contact Support</h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">Fill out the form below and we'll get back to you as soon as possible.</p>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-3xl p-8 md:p-12 border border-gray-100 dark:border-gray-700 shadow-sm">
        <form method="post" action="{% url 'support_contact' %}" class="space-y-6">
            {% csrf_token %}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Your Name</label>
                    <input type="text" name="name" required class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email Address</label>
                    <input type="email" name="email" required class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition">
                </div>
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">How can we help?</label>
                <select name="ticket_type" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition">
                    <option value="general">General Inquiry</option>
                    <option value="price_error">Report Incorrect Price</option>
                    <option value="broken_link">Report Broken Link</option>
                    <option value="product_error">Report Incorrect Product Information</option>
                    <option value="feature">Feature Request</option>
                    <option value="feedback">General Feedback</option>
                </select>
            </div>
            
            <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Subject</label>
                <input type="text" name="subject" required class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition">
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Message</label>
                <textarea name="message" rows="5" required class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary outline-none transition resize-none"></textarea>
            </div>

            <button type="submit" class="w-full bg-primary hover:bg-blue-600 text-white font-semibold py-4 rounded-xl transition shadow-lg shadow-primary/30">Submit Ticket</button>
        </form>
    </div>
</div>
{% endblock %}
"""

legal_html = """{% extends 'base.html' %}
{% block title %}{{ document.title }} - ShopSense AI{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="mb-12">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-white mb-4">{{ document.title }}</h1>
        <p class="text-gray-500 dark:text-gray-400">Last updated: {{ document.last_updated|date:"F j, Y" }}</p>
    </div>

    <div class="prose prose-lg prose-blue dark:prose-invert max-w-none bg-white dark:bg-gray-800 p-8 md:p-12 rounded-3xl border border-gray-100 dark:border-gray-700 shadow-sm">
        {{ document.content|safe }}
    </div>
</div>
{% endblock %}
"""

with open(os.path.join(SUPPORT_DIR, 'help_center.html'), 'w') as f:
    f.write(help_center_html)
    
with open(os.path.join(SUPPORT_DIR, 'contact.html'), 'w') as f:
    f.write(contact_html)

with open(os.path.join(LEGAL_DIR, 'document.html'), 'w') as f:
    f.write(legal_html)

print("Frontend templates generated.")
