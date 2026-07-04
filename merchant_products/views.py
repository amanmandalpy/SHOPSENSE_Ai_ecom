from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import MerchantProduct

class MerchantProductDetailView(DetailView):
    model = MerchantProduct
    template_name = 'merchant_products/merchant_product_detail.html'
    context_object_name = 'merchant_product'

class MerchantProductRedirectView(DetailView):
    model = MerchantProduct
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        url = obj.affiliate_url if obj.affiliate_url else obj.merchant_product_url
        return redirect(url)
