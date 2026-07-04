from django.test import TestCase
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from products.models import Product
from stores.models import Store
from brands.models import Brand
from categories.models import Category
from merchant_products.models import MerchantProduct, StockStatus
from .models import PriceHistory
from .services import record_price_change, get_price_statistics

class PriceHistoryTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Samsung', slug='samsung')
        self.category = Category.objects.create(name='TV', slug='tv')
        self.product = Product.objects.create(name='QLED 4K', brand=self.brand, category=self.category, sku='SAM-QLED', status='ACTIVE')
        self.store = Store.objects.create(name='Amazon', slug='amazon')
        
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            store=self.store,
            merchant_product_url='https://amazon.com/samsung',
            current_price=Decimal('1000.00'),
            availability_status=StockStatus.IN_STOCK
        )

    def test_duplicate_prevention(self):
        # First record
        record1 = record_price_change(self.listing)
        self.assertEqual(PriceHistory.objects.count(), 1)
        
        # Exact same data, shouldn't create a new record
        record2 = record_price_change(self.listing)
        self.assertEqual(PriceHistory.objects.count(), 1)
        self.assertEqual(record1.pk, record2.pk)

    def test_price_change_recording(self):
        record1 = record_price_change(self.listing)
        
        # Price drops
        self.listing.current_price = Decimal('800.00')
        self.listing.save()
        record2 = record_price_change(self.listing)
        
        self.assertEqual(PriceHistory.objects.count(), 2)
        self.assertNotEqual(record1.pk, record2.pk)
        
    def test_statistics_calculation(self):
        # Insert historical data simulating days ago
        now = timezone.now()
        PriceHistory.objects.create(merchant_product=self.listing, price=Decimal('1200.00'), recorded_at=now - timedelta(days=40))
        PriceHistory.objects.create(merchant_product=self.listing, price=Decimal('1000.00'), recorded_at=now - timedelta(days=10))
        PriceHistory.objects.create(merchant_product=self.listing, price=Decimal('900.00'), recorded_at=now - timedelta(days=2))
        
        stats = get_price_statistics(self.listing)
        
        # All time lowest is 900, highest is 1200
        self.assertEqual(stats['all_time']['lowest'], Decimal('900.00'))
        self.assertEqual(stats['all_time']['highest'], Decimal('1200.00'))
        
        # 30 day highest is 1000 (1200 was 40 days ago)
        self.assertEqual(stats['thirty_days']['highest'], Decimal('1000.00'))
        
        # Drop percentage from 1200 to 900 = 25%
        self.assertEqual(stats['price_drop_percentage'], 25.0)
