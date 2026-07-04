from django.test import TestCase
from affiliate.models import Merchant
from .models import MerchantFeed, FeedType

class MerchantFeedTestCase(TestCase):
    def test_feed_creation(self):
        merchant = Merchant.objects.create(name='Flipkart')
        feed = MerchantFeed.objects.create(
            merchant=merchant,
            name='Flipkart Main Feed',
            feed_type=FeedType.CSV,
            feed_url='https://flipkart.com/feed.csv'
        )
        self.assertEqual(feed.merchant.name, 'Flipkart')
        self.assertEqual(feed.feed_type, FeedType.CSV)
