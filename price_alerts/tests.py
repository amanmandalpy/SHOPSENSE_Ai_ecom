from django.test import TestCase, override_settings
from decimal import Decimal
from accounts.models import User
from products.models import Product
from stores.models import Store
from brands.models import Brand
from categories.models import Category
from merchant_products.models import MerchantProduct, StockStatus
from .models import PriceAlert, AlertStatus, AlertType
from .tasks import process_active_price_alerts
from notifications.models import Notification
from django.core.exceptions import ValidationError

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PriceAlertTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alertuser', email='alert@test.com', password='password123')
        self.brand = Brand.objects.create(name='Apple', slug='apple')
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.product = Product.objects.create(name='MacBook Air', brand=self.brand, category=self.category, sku='MAC-AIR', status='ACTIVE')
        self.store = Store.objects.create(name='Apple Store', slug='apple-store')
        
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            store=self.store,
            merchant_product_url='https://apple.com/macbook',
            current_price=Decimal('999.00'),
            availability_status=StockStatus.IN_STOCK
        )

    def test_duplicate_active_alert_prevention(self):
        # Create first alert
        alert1 = PriceAlert(user=self.user, merchant_product=self.listing, target_price=Decimal('899.00'))
        alert1.full_clean()
        alert1.save()
        
        # Try to create identical active alert
        alert2 = PriceAlert(user=self.user, merchant_product=self.listing, target_price=Decimal('799.00'))
        with self.assertRaises(ValidationError):
            alert2.full_clean()

    def test_alert_trigger_and_notification(self):
        alert = PriceAlert.objects.create(
            user=self.user,
            merchant_product=self.listing,
            target_price=Decimal('899.00')
        )
        
        # Initial run: Price is 999, Target is 899. Should not trigger.
        process_active_price_alerts.delay()
        alert.refresh_from_db()
        self.assertEqual(alert.status, AlertStatus.ACTIVE)
        self.assertEqual(Notification.objects.count(), 0)
        
        # Simulate price drop to exactly target
        self.listing.current_price = Decimal('899.00')
        self.listing.save()
        
        process_active_price_alerts.delay()
        alert.refresh_from_db()
        self.assertEqual(alert.status, AlertStatus.TRIGGERED)
        self.assertTrue(alert.notification_sent)
        self.assertIsNotNone(alert.triggered_at)
        
        # Verify notification created
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, self.user)
        self.assertIn("has dropped", notif.message)
