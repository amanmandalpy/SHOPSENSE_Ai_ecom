from django.urls import path
from .views import MyAlertsView, PriceAlertCreateView, toggle_alert_status, delete_alert

urlpatterns = [
    path('', MyAlertsView.as_view(), name='my_alerts'),
    path('create/', PriceAlertCreateView.as_view(), name='create_alert'),
    path('<int:pk>/toggle/', toggle_alert_status, name='toggle_alert'),
    path('<int:pk>/delete/', delete_alert, name='delete_alert'),
]
