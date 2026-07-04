from django.test import TestCase
from django.contrib.auth import get_user_model
from wishlist.models import Wishlist, WishlistItem
from products.models import Product
from brands.models import Brand
from categories.models import Category
from django.db import IntegrityError

User = get_user_model()

class WishlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pw')
        self.brand = Brand.objects.create(name='B', slug='b')
        self.cat = Category.objects.create(name='C', slug='c')
        self.product = Product.objects.create(name='Test', sku='test1', brand=self.brand, category=self.cat)

    def test_deduplication(self):
        wl = Wishlist.objects.create(user=self.user)
        WishlistItem.objects.create(wishlist=wl, product=self.product)
        
        with self.assertRaises(IntegrityError):
            WishlistItem.objects.create(wishlist=wl, product=self.product)
