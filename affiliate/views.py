from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from merchant_products.models import MerchantProduct
from .services import DeepLinkService, AffiliateService

class AffiliateRedirectView(View):
    def get(self, request, listing_id):
        listing = get_object_or_404(MerchantProduct, pk=listing_id)
        
        # 1. Generate Deep Link dynamically
        outbound_url = DeepLinkService.generate_affiliate_url(listing)
        
        # 2. Log Outbound Click synchronously
        AffiliateService.log_click(request, listing, outbound_url)
        
        # 3. Transparent Redirect
        return HttpResponseRedirect(outbound_url)
