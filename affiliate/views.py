from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from merchant_products.models import MerchantProduct
from affiliate.redirect_service import AffiliateRedirectService

class OutboundRedirectView(View):
    def get(self, request, *args, **kwargs):
        merchant_product_id = kwargs.get('pk')
        if not merchant_product_id:
            return HttpResponseBadRequest("Missing product identifier.")
            
        merchant_product = get_object_or_404(MerchantProduct, pk=merchant_product_id)
        
        # Security: ensure merchant is active
        if merchant_product.merchant.status != 'ACTIVE':
            return HttpResponseNotFound("Merchant is not active.")
            
        final_url = AffiliateRedirectService.generate_redirect_url_and_track(merchant_product, request)
        
        if not final_url:
            return HttpResponseBadRequest("Invalid destination URL.")
            
        # HTTP 302 Found (Standard for affiliate redirects)
        return redirect(final_url)
