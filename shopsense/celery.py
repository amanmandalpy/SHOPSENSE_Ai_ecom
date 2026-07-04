import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsense.settings.development')

app = Celery('shopsense')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
