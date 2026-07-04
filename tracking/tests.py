import uuid
from django.test import TestCase, RequestFactory
from affiliate.models import Merchant, AffiliateAccount
from products.models import Product, Brand
from categories.models import Category
from merchant_products.models import MerchantProduct
from tracking.models import AffiliateClick, ClickSession
from affiliate.redirect_service import AffiliateRedirectService
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

class TrackingTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.merchant = Merchant.objects.create(name='Amazon', status='ACTIVE')
        self.affiliate = AffiliateAccount.objects.create(merchant=self.merchant, tracking_id='shop-21', commission_status='ACTIVE')
        self.brand = Brand.objects.create(name='Apple', )
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(name='AirPods', slug='airpods', brand=self.brand, category=self.category)
        self.listing = MerchantProduct.objects.create(
            merchant=self.merchant,
            product=self.product,
            merchant_sku='A123',
            merchant_price=100.00,
            merchant_product_url='https://amazon.com/airpods'
        )
        
    def _add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()

    def test_redirect_service_amazon(self):
        request = self.factory.get('/out/1/?utm_source=fb&utm_campaign=summer')
        self._add_session_to_request(request)
        
        final_url = AffiliateRedirectService.generate_redirect_url_and_track(self.listing, request)
        
        # Test Affiliate URL logic
        self.assertEqual(final_url, 'https://amazon.com/airpods?tag=shop-21')
        
        # Test Click Tracking
        click = AffiliateClick.objects.first()
        self.assertIsNotNone(click)
        self.assertEqual(click.merchant, self.merchant)
        self.assertEqual(click.product, self.product)
        self.assertEqual(click.utm_source, 'fb')
        self.assertEqual(click.utm_campaign, 'summer')
        
        # Test Session Tracking
        session = ClickSession.objects.first()
        self.assertIsNotNone(session)
        self.assertEqual(session.clicks_count, 1)

    def test_redirect_view(self):
        response = self.client.get(reverse('affiliate:outbound_redirect', kwargs={'pk': self.listing.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://amazon.com/airpods?tag=shop-21')
