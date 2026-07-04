from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from products.models import Product
from brands.models import Brand
from categories.models import Category
from stores.models import Store
from merchant_products.models import MerchantProduct, StockStatus
from coupons.models import Coupon, DiscountType as CouponDiscountType, CouponStatus
from offers.models import BankOffer, DiscountType as OfferDiscountType, OfferType
from offers.services import calculate_best_savings

class SavingsEngineTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Apple', slug='apple')
        self.cat = Category.objects.create(name='Electronics', slug='electronics')
        self.store = Store.objects.create(name='iStore', slug='istore')
        
        self.product = Product.objects.create(name='iPhone 15', brand=self.brand, category=self.cat, sku='IP15', status='ACTIVE')
        
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            store=self.store,
            current_price=Decimal('1000.00'),
            availability_status=StockStatus.IN_STOCK
        )

    def test_flat_coupon_and_percentage_bank_offer(self):
        # Coupon: Flat 50 off
        Coupon.objects.create(
            code='SAVE50',
            name='Flat 50 Off',
            store=self.store,
            discount_type=CouponDiscountType.FLAT,
            discount_value=Decimal('50.00'),
            valid_until=timezone.now() + timedelta(days=5),
            status=CouponStatus.ACTIVE
        )
        
        # Bank Offer: 10% off up to max 100
        BankOffer.objects.create(
            name='HDFC 10% Off',
            bank_name='HDFC',
            store=self.store,
            offer_type=OfferType.BANK_DISCOUNT,
            discount_type=OfferDiscountType.PERCENTAGE,
            discount_value=Decimal('10.00'),
            max_discount=Decimal('100.00'),
            valid_until=timezone.now() + timedelta(days=5),
            is_active=True
        )
        
        # Expected calculation:
        # Initial Price: 1000.00
        # Coupon saves: 50.00 => Intermediate Price = 950.00
        # Bank saves: 10% of 950 = 95.00 (within 100 max bound) => Final = 950 - 95 = 855.00
        
        savings = calculate_best_savings(self.listing)
        
        self.assertEqual(savings['coupon_savings'], Decimal('50.00'))
        self.assertEqual(savings['bank_savings'], Decimal('95.00'))
        self.assertEqual(savings['final_effective_price'], Decimal('855.00'))
        self.assertEqual(savings['total_savings'], Decimal('145.00'))

    def test_expired_coupon_ignored(self):
        # Coupon: Flat 200 off (Expired)
        Coupon.objects.create(
            code='SAVE200',
            name='Flat 200 Off',
            store=self.store,
            discount_type=CouponDiscountType.FLAT,
            discount_value=Decimal('200.00'),
            valid_until=timezone.now() - timedelta(days=5),
            status=CouponStatus.ACTIVE
        )
        
        savings = calculate_best_savings(self.listing)
        self.assertEqual(savings['coupon_savings'], Decimal('0.00'))
        self.assertEqual(savings['final_effective_price'], Decimal('1000.00'))
