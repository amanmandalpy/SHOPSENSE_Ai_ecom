from django.test import TestCase
from django.urls import reverse
from brands.models import Brand
from categories.models import Category
from .models import Product, ProductTag, ProductSpecification

class ProductTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Apple', slug='apple')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.tag = ProductTag.objects.create(name='Smartphone')
        
        self.product = Product.objects.create(
            name='iPhone 15 Pro',
            brand=self.brand,
            category=self.category,
            sku='APPL-IP15P-128',
            status='ACTIVE'
        )
        self.product.tags.add(self.tag)
        
        self.spec = ProductSpecification.objects.create(
            product=self.product,
            key='Processor',
            value='A17 Pro'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.slug, 'iphone-15-pro')
        self.assertEqual(self.product.status, 'ACTIVE')
        self.assertIn(self.tag, self.product.tags.all())

    def test_duplicate_sku(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                name='Another iPhone',
                brand=self.brand,
                category=self.category,
                sku='APPL-IP15P-128'
            )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15 Pro')

    def test_product_search(self):
        response = self.client.get(reverse('product_list') + '?q=Apple')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15 Pro')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15 Pro')
        self.assertContains(response, 'A17 Pro')
