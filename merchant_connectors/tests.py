from django.test import TestCase
from stores.models import Store
from merchant_connectors.models import MerchantConnector, MerchantSyncLog
from merchant_connectors.services import MerchantSyncService

class MerchantConnectorTestCase(TestCase):
    def setUp(self):
        self.store = Store.objects.create(name='Amazon', slug='amazon', website_url='https://amazon.com')
        self.connector = MerchantConnector.objects.create(
            store=self.store,
            api_url='https://api.amazon.com'
        )

    def test_merchant_sync(self):
        MerchantSyncService.run_sync(self.connector, 'PRODUCTS')
        self.assertEqual(MerchantSyncLog.objects.count(), 1)
        log = MerchantSyncLog.objects.first()
        self.assertEqual(log.status, 'SUCCESS')
        
        self.connector.refresh_from_db()
        self.assertIsNotNone(self.connector.last_sync_time)
