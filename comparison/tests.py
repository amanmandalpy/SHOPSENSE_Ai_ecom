from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, ProductSpecification
from brands.models import Brand
from categories.models import Category
from comparison.models import ComparisonList, ComparisonItem
from comparison.services import get_or_create_comparison_list, add_product_to_compare, get_dynamic_comparison_matrix

class ComparisonTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='TechBrand', slug='tech')
        self.cat = Category.objects.create(name='Electronics', slug='electronics')
        self.client = Client()
        
        self.products = []
        for i in range(5):
            p = Product.objects.create(name=f'Product {i}', brand=self.brand, category=self.cat, sku=f'SKU-{i}', status='ACTIVE')
            self.products.append(p)
            
        ProductSpecification.objects.create(product=self.products[0], key='RAM', value='8GB')
        ProductSpecification.objects.create(product=self.products[1], key='Processor', value='Intel i5')
        ProductSpecification.objects.create(product=self.products[2], key='RAM', value='16GB')
        ProductSpecification.objects.create(product=self.products[2], key='Storage', value='512GB SSD')

    def test_max_four_constraint(self):
        # We simulate a request to the service
        class MockRequest:
            user = type('MockUser', (), {'is_authenticated': False})()
            session = type('MockSession', (), {'session_key': 'test1234', 'create': lambda: None})()
            
        req = MockRequest()
        
        add_product_to_compare(req, self.products[0].id)
        add_product_to_compare(req, self.products[1].id)
        add_product_to_compare(req, self.products[2].id)
        add_product_to_compare(req, self.products[3].id)
        
        with self.assertRaises(ValueError):
            add_product_to_compare(req, self.products[4].id)
            
        comp_list = ComparisonList.objects.get(session_key='test1234')
        self.assertEqual(comp_list.items.count(), 4)

    def test_dynamic_specification_matrix(self):
        class MockRequest:
            user = type('MockUser', (), {'is_authenticated': False})()
            session = type('MockSession', (), {'session_key': 'test1234', 'create': lambda: None})()
        req = MockRequest()
        
        add_product_to_compare(req, self.products[0].id)
        add_product_to_compare(req, self.products[1].id)
        add_product_to_compare(req, self.products[2].id)
        
        comp_list = ComparisonList.objects.get(session_key='test1234')
        matrix_data = get_dynamic_comparison_matrix(comp_list)
        
        specs = matrix_data['specifications']
        
        self.assertIn('RAM', specs)
        self.assertIn('Processor', specs)
        self.assertIn('Storage', specs)
        
        # Product 0 has RAM 8GB, no Processor, no Storage
        self.assertEqual(specs['RAM'][0], '8GB')
        self.assertEqual(specs['Processor'][0], '-')
        self.assertEqual(specs['Storage'][0], '-')
        
        # Product 2 has RAM 16GB, Storage 512GB
        self.assertEqual(specs['RAM'][2], '16GB')
        self.assertEqual(specs['Storage'][2], '512GB SSD')
