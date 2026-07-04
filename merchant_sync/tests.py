import os
import json
import csv
from django.test import TestCase
from affiliate.models import Merchant
from merchant_feeds.models import MerchantFeed, FeedType, FeedStatus
from merchant_sync.models import MerchantImportJob, JobStatus
from merchant_sync.services.feed_parser import FeedParserService
from merchant_sync.services.normalization import NormalizationService
from merchant_sync.services.import_service import ImportService
from products.models import Product
from merchant_products.models import MerchantProduct

class MerchantSyncTestCase(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name='Amazon')
        self.feed = MerchantFeed.objects.create(
            merchant=self.merchant,
            name='Test Feed',
            feed_type=FeedType.JSON,
            feed_url='file:///tmp/test_feed.json',
            status=FeedStatus.ACTIVE
        )
        self.sample_data = [
            {
                "sku": "AMZ-123",
                "title": "Sony Headphones",
                "brand": "Sony",
                "category": "Electronics",
                "price": "299.99",
                "original_price": "399.99",
                "stock": "in stock",
                "url": "https://amazon.com/sony"
            }
        ]
        self.test_file_path = 'test_feed.json'
        with open(self.test_file_path, 'w') as f:
            json.dump(self.sample_data, f)
            
        self.feed.feed_url = f"file://{os.path.abspath(self.test_file_path)}"
        self.feed.save()

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_feed_parser(self):
        items = list(FeedParserService.parse_feed(self.test_file_path, FeedType.JSON))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['sku'], "AMZ-123")
        
    def test_normalization(self):
        norm = NormalizationService.normalize(self.sample_data[0])
        self.assertEqual(norm['sku'], "AMZ-123")
        self.assertEqual(norm['product_name'], "Sony Headphones")
        self.assertEqual(norm['price'], 299.99)
        self.assertEqual(norm['stock'], "IN_STOCK")
        
    def test_import_service(self):
        job = MerchantImportJob.objects.create(merchant=self.merchant, feed=self.feed)
        service = ImportService(job)
        service.execute()
        
        job.refresh_from_db()
        self.assertEqual(job.status, JobStatus.COMPLETED)
        self.assertEqual(job.imported_count, 1)
        
        # Verify DB
        self.assertTrue(Product.objects.filter(sku='AMZ-123').exists())
        self.assertTrue(MerchantProduct.objects.filter(merchant_sku='AMZ-123').exists())
        
        # Test Duplicate skipping
        job2 = MerchantImportJob.objects.create(merchant=self.merchant, feed=self.feed)
        service2 = ImportService(job2)
        service2.execute()
        job2.refresh_from_db()
        self.assertEqual(job2.updated_count, 1)
        self.assertEqual(job2.imported_count, 0)
