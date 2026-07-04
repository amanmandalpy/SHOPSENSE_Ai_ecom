from django.test import TestCase
from analytics.models import ProductAnalytics, PlatformEvent, EventType, MerchantAnalytics
from tracking.models import AffiliateClick, ClickSession
from affiliate.models import Merchant
from products.models import Product, Brand
from categories.models import Category
from analytics.services import AnalyticsAggregationService
from django.utils import timezone

class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name='Amazon')
        self.brand = Brand.objects.create(name='Apple')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(name='AirPods', brand=self.brand, category=self.category)
        self.session = ClickSession.objects.create(session_identifier='s-123')
        
        # 100 views
        for i in range(100):
            PlatformEvent.objects.create(
                event_type=EventType.PRODUCT_VIEW,
                metadata={'product_id': self.product.id}
            )
            
        # 5 clicks
        for i in range(5):
            AffiliateClick.objects.create(
                merchant=self.merchant,
                product=self.product,
                session=self.session
            )

    def test_ctr_calculation(self):
        AnalyticsAggregationService.calculate_product_ctrs()
        
        pa = ProductAnalytics.objects.get(product=self.product)
        self.assertEqual(pa.views_count, 100)
        self.assertEqual(pa.affiliate_clicks, 5)
        self.assertEqual(float(pa.ctr), 5.00)

    def test_daily_merchant_analytics(self):
        AnalyticsAggregationService.aggregate_daily_merchant_analytics(timezone.now().date())
        
        ma = MerchantAnalytics.objects.get(merchant=self.merchant, date=timezone.now().date())
        self.assertEqual(ma.total_clicks, 5)
        self.assertEqual(ma.unique_clicks, 1) # all shared same session
