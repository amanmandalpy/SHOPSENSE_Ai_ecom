from django.urls import path
from .views import MerchantProductDetailView, MerchantProductRedirectView

urlpatterns = [
    path('<int:pk>/', MerchantProductDetailView.as_view(), name='merchant_product_detail'),
    path('<int:pk>/redirect/', MerchantProductRedirectView.as_view(), name='merchant_product_redirect'),
]
