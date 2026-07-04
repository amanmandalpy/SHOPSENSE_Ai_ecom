import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsense.settings')
django.setup()

from support.models import FAQCategory, FAQ

def seed_faqs():
    # Categories
    cat_general, _ = FAQCategory.objects.get_or_create(
        name='General Questions', 
        defaults={'icon': 'fa-solid fa-circle-question', 'order': 1, 'slug': 'general-questions'}
    )
    cat_ai, _ = FAQCategory.objects.get_or_create(
        name='AI Shopping Assistant', 
        defaults={'icon': 'fa-solid fa-robot', 'order': 2, 'slug': 'ai-shopping-assistant'}
    )
    cat_price, _ = FAQCategory.objects.get_or_create(
        name='Pricing & Alerts', 
        defaults={'icon': 'fa-solid fa-bell', 'order': 3, 'slug': 'pricing-alerts'}
    )

    # FAQs - General
    FAQ.objects.update_or_create(
        question='Do you sell these products directly?',
        defaults={'category': cat_general, 'answer': 'No, ShopSense AI is a search and comparison engine. When you click "Buy Now", you are securely redirected to the official retailer (like Amazon or Flipkart) where you complete your transaction.', 'is_published': True}
    )
    FAQ.objects.update_or_create(
        question='Is ShopSense AI completely free to use?',
        defaults={'category': cat_general, 'answer': 'Yes! Our platform is 100% free for shoppers. We make money through small affiliate commissions paid by the retailers when you make a purchase, at absolutely zero extra cost to you.', 'is_published': True}
    )
    
    # FAQs - AI
    FAQ.objects.update_or_create(
        question='How does the AI Assistant know which product is best?',
        defaults={'category': cat_ai, 'answer': 'Our AI analyzes millions of data points including spec sheets, price histories, expert reviews, and user feedback. It ignores marketing fluff and ranks products purely based on objective features and your specific budget constraints.', 'is_published': True}
    )
    FAQ.objects.update_or_create(
        question='Can I ask the AI conversational questions?',
        defaults={'category': cat_ai, 'answer': 'Absolutely. You can ask things like "What is the best laptop under $1000 for video editing?" or "Is the iPhone 15 better than the Samsung S24 for photography?" and our AI will give you a direct, reasoned answer.', 'is_published': True}
    )

    # FAQs - Pricing
    FAQ.objects.update_or_create(
        question='How accurate is the price tracking?',
        defaults={'category': cat_price, 'answer': 'We sync our prices constantly with official retailer APIs and XML feeds. However, flash sales and lightning deals can expire in minutes. The final price shown on the checkout page of the retailer is the official price.', 'is_published': True}
    )
    FAQ.objects.update_or_create(
        question='How do Price Alerts work?',
        defaults={'category': cat_price, 'answer': 'Simply click the "Alert Me" button on any product page and set your target price. When the product drops below your target across any of our tracked merchants, we will instantly send you an email notification so you can secure the deal.', 'is_published': True}
    )
    
    print("FAQs seeded successfully.")

seed_faqs()
