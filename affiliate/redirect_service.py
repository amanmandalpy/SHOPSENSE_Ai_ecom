from django.utils import timezone
from affiliate.models import AffiliateAccount
from merchant_products.models import MerchantProduct
from tracking.models import AffiliateClick, ClickSession, UTMSource, Campaign
import uuid

class AffiliateRedirectService:
    @staticmethod
    def generate_redirect_url_and_track(merchant_product: MerchantProduct, request):
        """
        Validates the merchant product, generates the affiliate tracking URL,
        records the click analytics, and returns the final destination URL.
        """
        merchant = merchant_product.merchant
        original_url = merchant_product.merchant_product_url
        
        # 1. Generate Final Affiliate URL
        try:
            account = AffiliateAccount.objects.get(merchant=merchant, commission_status='ACTIVE')
            affiliate_url = AffiliateRedirectService._build_affiliate_url(original_url, account)
        except AffiliateAccount.DoesNotExist:
            affiliate_url = original_url # Fallback if no active affiliate account
            
        # 2. Extract Request Data
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            
        ip_address = AffiliateRedirectService._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Determine Device
        device_type = 'Desktop'
        if 'Mobile' in user_agent:
            device_type = 'Mobile'
        elif 'Tablet' in user_agent:
            device_type = 'Tablet'
            
        # 3. UTM Parameters
        utm_source = request.GET.get('utm_source', '')
        utm_medium = request.GET.get('utm_medium', '')
        utm_campaign = request.GET.get('utm_campaign', '')
        
        # Optional: Resolve Campaign DB object if we want strict relational tracking
        campaign_obj = None
        if utm_campaign:
            campaign_obj = Campaign.objects.filter(code=utm_campaign).first()
            
        # 4. Session Tracking
        # Create or update ClickSession
        click_session, created = ClickSession.objects.get_or_create(
            session_identifier=session_id,
            defaults={
                'visitor_identifier': request.COOKIES.get('visitor_id', str(uuid.uuid4())),
                'entry_page': referrer
            }
        )
        click_session.clicks_count += 1
        click_session.save(update_fields=['clicks_count', 'updated_at'])
        
        # 5. Record Click
        AffiliateClick.objects.create(
            user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
            session=click_session,
            merchant=merchant,
            merchant_product=merchant_product,
            product=merchant_product.product,
            affiliate_url=affiliate_url,
            original_merchant_url=original_url,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            campaign=campaign_obj,
            ip_address=ip_address,
            device_type=device_type,
            browser=user_agent[:100], # Simplify browser parsing
            referrer=referrer
        )
        
        return affiliate_url

    @staticmethod
    def _build_affiliate_url(base_url, account: AffiliateAccount):
        """Appends proper tracking parameters based on official merchant TOS."""
        if not base_url:
            return ""
            
        # Extremely simplified logic for demonstration:
        separator = '&' if '?' in base_url else '?'
        
        if account.merchant.name.lower() == 'amazon':
            return f"{base_url}{separator}tag={account.tracking_id}"
        elif account.merchant.name.lower() == 'flipkart':
            return f"{base_url}{separator}affid={account.tracking_id}"
        
        # Generic fallback
        return f"{base_url}{separator}ref={account.tracking_id}"

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
