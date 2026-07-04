from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Category

class CategoryTestCase(TestCase):
    def setUp(self):
        self.electronics = Category.objects.create(name='Electronics', slug='electronics')
        self.phones = Category.objects.create(name='Phones', slug='phones', parent=self.electronics)

    def test_hierarchy(self):
        self.assertEqual(self.phones.parent, self.electronics)
        self.assertIn(self.phones, self.electronics.children.all())

    def test_duplicate_name(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Electronics', slug='electronics-2')

    def test_duplicate_slug(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Electronics 2', slug='electronics')

    def test_self_parent_validation(self):
        self.electronics.parent = self.electronics
        with self.assertRaises(ValidationError):
            self.electronics.clean()

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electronics')

    def test_category_detail_view(self):
        response = self.client.get(self.electronics.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electronics')
