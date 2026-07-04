from django.test import TestCase
from django.urls import reverse
from .models import Brand

class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Apple', slug='apple', country='USA', founded_year=1976)

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, 'Apple')
        self.assertEqual(self.brand.slug, 'apple')

    def test_duplicate_name(self):
        with self.assertRaises(Exception):
            Brand.objects.create(name='Apple', slug='apple-2')

    def test_brand_list_view(self):
        response = self.client.get(reverse('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')

    def test_brand_detail_view(self):
        response = self.client.get(self.brand.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')
