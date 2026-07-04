from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .models import AffiliateConfig, AffiliateClick

class DeepLinkService:
    @staticmethod
    def generate_affiliate_url(merchant_product):
        base_url = merchant_product.merchant_product_url
        try:
            config = AffiliateConfig.objects.get(store=merchant_product.store, is_active=True)
            
            # Parse existing URL
            url_parts = list(urlparse(base_url))
            query = dict(parse_qs(url_parts[4]))
            
            # Inject tracking parameter
            query.update({config.tracking_param_name: config.affiliate_id})
            url_parts[4] = urlencode(query, doseq=True)
            
            return urlunparse(url_parts)
            
        except AffiliateConfig.DoesNotExist:
            return base_url

class AffiliateService:
    @staticmethod
    def log_click(request, merchant_product, outbound_url):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        device = request.META.get('HTTP_USER_AGENT', '')[:200]
        
        AffiliateClick.objects.create(
            user=request.user if request.user.is_authenticated else None,
            merchant_product=merchant_product,
            outbound_url=outbound_url,
            ip_address=ip,
            device=device,
            browser=device
        )
