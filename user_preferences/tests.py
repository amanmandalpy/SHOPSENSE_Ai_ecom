from django.test import TestCase
from django.contrib.auth import get_user_model
from user_preferences.models import BrowsingHistory
from products.models import Product
from brands.models import Brand
from categories.models import Category
from recommendation.services import PersonalizationEngine

User = get_user_model()

class PersonalizationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pw')
        self.brand = Brand.objects.create(name='B', slug='b')
        self.cat = Category.objects.create(name='C', slug='c')
        self.product1 = Product.objects.create(name='P1', sku='p1', brand=self.brand, category=self.cat)

    def test_browsing_history_limit(self):
        for i in range(55):
            p = Product.objects.create(name=f'Px{i}', sku=f'sku{i}', brand=self.brand, category=self.cat)
            PersonalizationEngine.log_product_view(self.user, p)
            
        count = BrowsingHistory.objects.filter(user=self.user).count()
        self.assertEqual(count, 50)
