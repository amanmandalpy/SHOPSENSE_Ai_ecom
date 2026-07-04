from django.test import TestCase
from affiliate.models import Merchant, AffiliateAccount
from tracking.models import AffiliateClick
from affiliate.services import AffiliateService
from merchant_products.models import MerchantProduct
from products.models import Product
from brands.models import Brand
from categories.models import Category

class AffiliateTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='B', slug='b')
        self.cat = Category.objects.create(name='C', slug='c')
        self.merchant = Merchant.objects.create(name='Amazon', website='https://amazon.com')
        self.config = AffiliateAccount.objects.create(
            merchant=self.merchant,
            affiliate_id='shopsense-20',
            tracking_parameters={'tag': 'shopsense-20'},
            commission_status='ACTIVE'
        )
        self.product = Product.objects.create(name='Test Product', sku='test-1', brand=self.brand, category=self.cat)
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            merchant=self.merchant,
            merchant_sku='merch-1',
            merchant_product_url='https://amazon.com/dp/123',
            merchant_price=10.00
        )

    def test_generate_affiliate_link(self):
        url = AffiliateService.generate_affiliate_link(self.listing)
        self.assertTrue('tag=shopsense-20' in url)
        self.assertTrue(AffiliateClick.objects.count() == 1)
