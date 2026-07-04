import os

TEMPLATE_DIR = 'd:\\PYTHON_PROJECTS\\SHOPSENSE_Ai_ecommerce\\templates'

def create_error_template(filename, code, title, message):
    content = f"""{{% extends 'base.html' %}}
{{% block title %}}{code} {title} - ShopSense AI{{% endblock %}}

{{% block content %}}
<div class="min-h-[70vh] flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-max mx-auto text-center">
        <main class="sm:flex">
            <p class="text-4xl font-extrabold text-primary sm:text-5xl">{code}</p>
            <div class="sm:ml-6">
                <div class="sm:border-l sm:border-gray-200 sm:pl-6">
                    <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight sm:text-5xl">{title}</h1>
                    <p class="mt-1 text-base text-gray-500 dark:text-gray-400">{message}</p>
                </div>
                <div class="mt-10 flex space-x-3 sm:border-l sm:border-transparent sm:pl-6 justify-center sm:justify-start">
                    <a href="{{% url 'home' %}}" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                        Go back home
                    </a>
                    <a href="{{% url 'support_home' %}}" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-primary bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                        Contact support
                    </a>
                </div>
            </div>
        </main>
    </div>
</div>
{{% endblock %}}"""
    with open(os.path.join(TEMPLATE_DIR, filename), 'w') as f:
        f.write(content)

create_error_template('404.html', '404', 'Page not found', 'Please check the URL in the address bar and try again.')
create_error_template('403.html', '403', 'Access denied', 'You do not have permission to access this resource.')
create_error_template('500.html', '500', 'Internal Server Error', 'Something went wrong on our end. We are looking into it.')

maintenance_content = """{% extends 'base.html' %}
{% block title %}Maintenance - ShopSense AI{% endblock %}

{% block content %}
<div class="min-h-[70vh] flex items-center justify-center px-4 sm:px-6 lg:px-8 text-center">
    <div>
        <div class="text-primary text-6xl mb-6"><i class="fa-solid fa-wrench"></i></div>
        <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">We'll be right back</h1>
        <p class="text-xl text-gray-500 dark:text-gray-400 mb-8">ShopSense AI is currently undergoing scheduled maintenance.<br>Thank you for your patience.</p>
    </div>
</div>
{% endblock %}"""
with open(os.path.join(TEMPLATE_DIR, 'maintenance.html'), 'w') as f:
    f.write(maintenance_content)

print("Error templates created.")
