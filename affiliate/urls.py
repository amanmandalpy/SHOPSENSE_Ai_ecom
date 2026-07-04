from django.urls import path
from .views import OutboundRedirectView

app_name = 'affiliate'

urlpatterns = [
    path('<int:pk>/', OutboundRedirectView.as_view(), name='outbound_redirect'),
]
