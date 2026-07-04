from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from products.models import Product
from stores.models import Store
from brands.models import Brand
from categories.models import Category
from .models import MerchantProduct, StockStatus

class MerchantProductTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Sony', slug='sony')
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(name='WH-1000XM5', brand=self.brand, category=self.category, sku='SONY-XM5')
        self.store1 = Store.objects.create(name='Amazon', slug='amazon')
        self.store2 = Store.objects.create(name='Flipkart', slug='flipkart')
        
        self.listing1 = MerchantProduct.objects.create(
            product=self.product,
            store=self.store1,
            merchant_product_url='https://amazon.com/sony',
            current_price=299.99,
            original_price=399.99,
            availability_status=StockStatus.IN_STOCK
        )

    def test_discount_calculation(self):
        self.listing1.refresh_from_db()
        self.assertAlmostEqual(float(self.listing1.discount_percentage), 25.0, places=1)

    def test_duplicate_mapping_prevention(self):
        with self.assertRaises(IntegrityError):
            MerchantProduct.objects.create(
                product=self.product,
                store=self.store1,
                merchant_product_url='https://amazon.com/sony-2',
                current_price=250.00
            )

    def test_negative_price_validation(self):
        listing = MerchantProduct(
            product=self.product,
            store=self.store2,
            merchant_product_url='https://flipkart.com/sony',
            current_price=-10.00
        )
        with self.assertRaises(ValidationError):
            listing.full_clean()
            listing.save()

    def test_original_price_validation(self):
        listing = MerchantProduct(
            product=self.product,
            store=self.store2,
            merchant_product_url='https://flipkart.com/sony',
            current_price=300.00,
            original_price=200.00
        )
        with self.assertRaises(ValidationError):
            listing.full_clean()
            listing.save()
