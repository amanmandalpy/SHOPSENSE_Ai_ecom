from django.urls import path
from .views import media_manager_view, backup_manager_view

urlpatterns = [
    path('admin-extra/media/', media_manager_view, name='media_manager'),
    path('admin-extra/backup/', backup_manager_view, name='backup_manager'),
]
