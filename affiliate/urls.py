from django.urls import path
from .views import AffiliateRedirectView

urlpatterns = [
    path('<int:listing_id>/', AffiliateRedirectView.as_view(), name='affiliate_redirect'),
]
