import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsense.settings')
django.setup()

from legal.models import LegalDocument

privacy_content = """
<h2>1. Introduction</h2>
<p>At ShopSense AI, your privacy is our priority. This Privacy Policy explains how we collect, use, and protect your personal information when you use our platform to compare prices, chat with our AI assistant, and discover products.</p>

<h2>2. Information We Collect</h2>
<ul>
    <li><strong>Account Information:</strong> When you register, we collect your name, email address, and password.</li>
    <li><strong>Usage Data:</strong> We automatically track the products you view, search queries, and your interactions with our AI Assistant to provide you with better recommendations.</li>
    <li><strong>Click Tracking:</strong> When you click on an outbound affiliate link, we record anonymized metadata (such as device type, browser, and generalized location) to monitor traffic quality.</li>
</ul>

<h2>3. How We Use Your Data</h2>
<p>Your data is strictly used to improve your shopping experience. We use your search history to recommend better deals, and your AI chat logs to refine our natural language processing models. We <strong>do not</strong> sell your personal data to third-party marketing agencies.</p>

<h2>4. Cookies & Tracking</h2>
<p>We use essential cookies to keep you logged in and track your Wishlist. We also use analytics cookies to understand how our platform is being used.</p>

<h2>5. Contact Us</h2>
<p>If you have questions about your privacy, please visit our <a href="/support/contact/">Contact Support</a> page.</p>
"""

terms_content = """
<h2>1. Acceptance of Terms</h2>
<p>By accessing and using ShopSense AI, you accept and agree to be bound by the terms and provision of this agreement.</p>

<h2>2. Description of Service</h2>
<p>ShopSense AI provides an AI-powered product search and comparison engine. We aggregate product data, pricing, and availability from third-party merchants (such as Amazon, Flipkart, etc.). <strong>We do not sell physical products directly.</strong> Any purchase you make is a transaction directly between you and the respective third-party merchant.</p>

<h2>3. Pricing & Availability Accuracy</h2>
<p>While our systems sync continuously, merchant prices and stock levels can change rapidly. We cannot guarantee that the price displayed on our site will be the exact price upon checkout on the merchant's website. The merchant's listed price is always the final authority.</p>

<h2>4. User Accounts</h2>
<p>You are responsible for maintaining the confidentiality of your account and password. ShopSense AI reserves the right to refuse service, terminate accounts, or remove content at our sole discretion.</p>
"""

affiliate_content = """
<h2>Honesty & Transparency</h2>
<p>ShopSense AI is a participant in various affiliate marketing programs. This means that when you click on links to various merchants on this site and make a purchase, this can result in a commission that is credited to ShopSense AI.</p>

<h2>How Does This Affect You?</h2>
<p>It doesn't! Our affiliate relationships do not influence the price you pay. You will pay the exact same price as you would if you navigated to the merchant's website directly. The small commissions we earn simply help us keep our servers running and our AI models improving.</p>

<h2>Our AI Integrity</h2>
<p>Unlike traditional review blogs that might push high-commission items, our AI Assistant and Comparison Engine are designed to be completely impartial. Our algorithms rank products based on features, price history, and relevance to your query—not on our potential payout.</p>

<p>Current affiliate programs we participate in include, but are not limited to, the Amazon Associates Program and the Flipkart Affiliate Program.</p>
"""

def seed_legal():
    LegalDocument.objects.update_or_create(
        slug='privacy-policy',
        defaults={'title': 'Privacy Policy', 'content': privacy_content, 'is_published': True}
    )
    LegalDocument.objects.update_or_create(
        slug='terms-of-service',
        defaults={'title': 'Terms of Service', 'content': terms_content, 'is_published': True}
    )
    LegalDocument.objects.update_or_create(
        slug='affiliate-disclosure',
        defaults={'title': 'Affiliate Disclosure', 'content': affiliate_content, 'is_published': True}
    )
    print("Legal documents seeded successfully.")

seed_legal()
