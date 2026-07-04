from django.test import TestCase
from products.models import Product
from brands.models import Brand
from categories.models import Category
from stores.models import Store
from merchant_products.models import MerchantProduct, StockStatus
from search.services import execute_search, log_search
from search.models import SearchQuery
from decimal import Decimal

class AdvancedSearchTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Sony', slug='sony')
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.store1 = Store.objects.create(name='Amazon', slug='amazon')
        
        self.product1 = Product.objects.create(name='WH-1000XM4', brand=self.brand, category=self.category, sku='SONY-XM4', status='ACTIVE')
        self.product2 = Product.objects.create(name='WH-1000XM5', brand=self.brand, category=self.category, sku='SONY-XM5', status='ACTIVE')
        
        MerchantProduct.objects.create(product=self.product1, store=self.store1, current_price=Decimal('250.00'), availability_status=StockStatus.IN_STOCK)
        MerchantProduct.objects.create(product=self.product2, store=self.store1, current_price=Decimal('350.00'), availability_status=StockStatus.IN_STOCK)

    def test_search_by_name(self):
        qs = execute_search('XM4')
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, 'WH-1000XM4')

    def test_search_by_brand_and_price_filter(self):
        filters = {'min_price': '300'}
        qs = execute_search('Sony', filters=filters)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, 'WH-1000XM5')

    def test_analytics_logging(self):
        log_search('Sony Headphones', 2)
        log_search('sony headphones ', 1)
        
        sq = SearchQuery.objects.get(keyword='sony headphones')
        self.assertEqual(sq.search_count, 2)
        self.assertEqual(sq.last_results_count, 1)

    def test_sorting(self):
        qs = execute_search('Sony', sort_by='lowest_price')
        self.assertEqual(qs.first().name, 'WH-1000XM4')
        
        qs_high = execute_search('Sony', sort_by='highest_price')
        self.assertEqual(qs_high.first().name, 'WH-1000XM5')
