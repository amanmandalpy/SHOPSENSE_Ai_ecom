from urllib.parse import urlencode, urlparse, parse_qs
from affiliate.models import AffiliateAccount
from tracking.models import AffiliateClick

class AffiliateService:
    @staticmethod
    def generate_affiliate_link(merchant_product, user=None, request=None):
        try:
            account = AffiliateAccount.objects.get(merchant=merchant_product.merchant, commission_status='ACTIVE')
            
            # Base URL is either deep link base or the merchant product URL
            base_url = account.deep_link_base_url if account.deep_link_base_url else merchant_product.merchant_product_url
            
            # Tracking params
            params = account.tracking_parameters.copy()
            if account.tracking_id:
                params['tracking_id'] = account.tracking_id
                
            if params:
                query_string = urlencode(params)
                if '?' in base_url:
                    final_url = f"{base_url}&{query_string}"
                else:
                    final_url = f"{base_url}?{query_string}"
            else:
                final_url = base_url
                
            # Log click
            ip_address = ''
            user_agent = ''
            if request:
                ip_address = request.META.get('REMOTE_ADDR', '')
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                
            AffiliateClick.objects.create(
                user=user,
                merchant=merchant_product.merchant,
                product=merchant_product.product,
                merchant_product=merchant_product,
                affiliate_url=final_url,
                original_merchant_url=merchant_product.merchant_product_url,
                ip_address=ip_address,
                browser=user_agent[:200]
            )
            
            return final_url
            
        except AffiliateAccount.DoesNotExist:
            # Fallback to direct merchant URL
            return merchant_product.merchant_product_url
