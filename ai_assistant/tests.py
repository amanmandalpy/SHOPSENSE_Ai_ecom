from django.test import TestCase
from decimal import Decimal
from unittest.mock import patch
from ai_assistant.scoring import ShoppingScoreService, ValueBadgeService
from ai_assistant.services import RecommendationService, PromptBuilderService
from ai_assistant.models import PromptTemplate, PromptCategory
from products.models import Product
from affiliate.models import Merchant
from merchant_products.models import MerchantProduct, StockStatus
from brands.models import Brand
from categories.models import Category
import json

class AIShoppingEngineTestCase(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name='Test Store')
        self.brand = Brand.objects.create(name='Sony')
        self.cat = Category.objects.create(name='TV')
        self.product = Product.objects.create(name='Ultra TV', sku='UTV1', status='ACTIVE', brand=self.brand, category=self.cat)
        self.listing = MerchantProduct.objects.create(
            product=self.product,
            merchant=self.merchant,
            merchant_price=Decimal('1000.00'),
            stock=StockStatus.IN_STOCK
        )

    def test_shopping_score_baseline(self):
        score = ShoppingScoreService.calculate_score(self.listing)
        # 50 is baseline for no discounts
        self.assertEqual(score, 50)
        
    def test_value_badge_service(self):
        # 100 score on a 500 budget item = Editor's Choice, Best Value, Best Budget
        badges = ValueBadgeService.get_badges(100, Decimal('500.00'))
        self.assertIn("Editor's Choice", badges)
        self.assertIn("Best Value", badges)
        self.assertIn("Best Budget", badges)
        self.assertNotIn("Best Premium", badges)

    def test_prompt_builder_service(self):
        PromptTemplate.objects.create(
            name="Default",
            category=PromptCategory.RECOMMENDATION,
            content="This is a dynamic prompt."
        )
        
        product_data = [{'id': '1', 'name': 'TV', 'price': '100', 'brand': 'Sony'}]
        sys_prompt, user_prompt = PromptBuilderService.build_prompt("Best TV", product_data)
        
        self.assertEqual(sys_prompt, "This is a dynamic prompt.")
        self.assertIn("Best TV", user_prompt)
        self.assertIn("ID: 1, Name: TV, Price: 100, Brand: Sony", user_prompt)

    @patch('ai_assistant.providers.MockProvider.generate_response')
    @patch('ai_assistant.services.execute_search')
    def test_recommendation_service_mapping(self, mock_search, mock_generate):
        mock_search.return_value = [self.product]
        
        # We need the provider to return JSON referencing self.listing.id
        mock_response = {
            "recommended_products": [str(self.listing.id)],
            "pros_cons": {str(self.listing.id): {"pros": ["Good"], "cons": ["None"]}},
            "buying_guide": "Buy this TV.",
            "reason": "It's good."
        }
        mock_generate.return_value = json.dumps(mock_response)
        
        service = RecommendationService(provider_name='mock')
        res = service.get_recommendations("Test Query")
        
        self.assertIn('mapped_recommendations', res)
        self.assertEqual(len(res['mapped_recommendations']), 1)
        
        mapped = res['mapped_recommendations'][0]
        self.assertEqual(mapped['listing'].id, self.listing.id)
        self.assertEqual(mapped['score'], 50)
        self.assertEqual(mapped['pros_cons']['pros'][0], "Good")
