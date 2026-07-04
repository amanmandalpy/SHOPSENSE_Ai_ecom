from django.test import TestCase
from affiliate.models import AffiliateConfig, AffiliateClick
from affiliate.services import DeepLinkService
from stores.models import Store
from merchant_products.models import MerchantProduct
from products.models import Product
from brands.models import Brand
from categories.models import Category

class AffiliateTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='B', slug='b')
        self.cat = Category.objects.create(name='C', slug='c')
        self.store = Store.objects.create(name='Amazon', slug='amazon', website_url='https://amazon.com')
        self.config = AffiliateConfig.objects.create(
            store=self.store,
            affiliate_id='shopsense-20',
            tracking_param_name='tag',
            is_active=True
        )
        self.product = Product.objects.create(name='Test Product', sku='test-1', brand=self.brand, category=self.cat)
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            store=self.store,
            merchant_sku='merch-1',
            merchant_product_url='https://www.amazon.com/dp/B08XJG8KVZ?ref=test',
            current_price=10.0
        )

    def test_deep_link_generation(self):
        generated_url = DeepLinkService.generate_affiliate_url(self.listing)
        self.assertIn('tag=shopsense-20', generated_url)
        self.assertIn('ref=test', generated_url)
