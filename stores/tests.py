from django.test import TestCase
from django.urls import reverse
from .models import Store

class StoreTestCase(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            name='Amazon',
            slug='amazon',
            website_url='https://amazon.in',
            country='India',
            rating=4.8
        )

    def test_store_creation(self):
        self.assertEqual(self.store.name, 'Amazon')
        self.assertEqual(self.store.currency, 'INR') # Default

    def test_duplicate_name(self):
        with self.assertRaises(Exception):
            Store.objects.create(name='Amazon', slug='amazon-2')

    def test_store_list_view(self):
        response = self.client.get(reverse('store_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amazon')

    def test_store_detail_view(self):
        response = self.client.get(self.store.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amazon')
