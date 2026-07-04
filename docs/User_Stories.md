# User Stories

This document contains 100 professional User Stories covering the core modules of ShopSense AI.

## Epic 1: Search & Discovery (1-15)
1. As a shopper, I want to search for a product by name so that I can quickly find its price.
2. As a shopper, I want search auto-suggestions as I type so that I save time.
3. As a shopper, I want typo tolerance in the search bar so that I find products even if I misspell them.
4. As a shopper, I want to filter search results by price range so that I stay within budget.
5. As a shopper, I want to filter by brand so that I only see brands I trust.
6. As a shopper, I want to filter by specifications (e.g., RAM) so that I find exact tech matches.
7. As a shopper, I want to sort results by "Price: Low to High" to find the cheapest option.
8. As a shopper, I want to sort by "Highest Rated" to find reliable products.
9. As a shopper, I want to see a product's main image in search results so that I can visually verify it.
10. As a shopper, I want to see a "Trending Searches" section so I know what's popular.
11. As a shopper, I want to browse products by category (e.g., Electronics, Fashion) for general discovery.
12. As a shopper, I want to see a "Deal of the Day" badge on highly discounted items.
13. As a shopper, I want to clear all active filters with one click so I can restart my search.
14. As a shopper, I want to see pagination or infinite scroll so I can view more results seamlessly.
15. As a shopper, I want to view search results on mobile without horizontal scrolling.

## Epic 2: Product & Price Comparison (16-30)
16. As a shopper, I want to view a dedicated product page with all merchant prices listed.
17. As a shopper, I want to see the merchant logos next to prices for instant recognition.
18. As a shopper, I want the lowest price highlighted in green so it catches my eye.
19. As a shopper, I want to read a consolidated AI summary of product reviews so I don't have to read 100s of comments.
20. As a shopper, I want to select multiple products and click "Compare" to see a side-by-side spec table.
21. As a shopper, I want the comparison table to highlight the "winner" for each spec row.
22. As a shopper, I want to remove an item from the comparison view easily.
23. As a shopper, I want to view high-resolution product images in a gallery slider.
24. As a shopper, I want to see official delivery estimates (if available) to know when I'll get it.
25. As a shopper, I want to see aggregated user ratings (out of 5 stars).
26. As a shopper, I want to share a product comparison link with my friend via WhatsApp.
27. As a shopper, I want to see alternative product recommendations ("Similar to this").
28. As a shopper, I want to see out-of-stock indicators clearly so I don't waste time clicking.
29. As a shopper, I want to view the product's official warranty information.
30. As a shopper, I want to see variations (color/storage) and how they affect the price.

## Epic 3: Price History & Alerts (31-45)
31. As a shopper, I want to view a line chart of the product's price history over the last 6 months.
32. As a shopper, I want to hover over the chart to see the exact price on a specific date.
33. As a shopper, I want the chart to indicate major sale events (e.g., Diwali Sale) as reference points.
34. As a user, I want to click "Set Price Alert" on any product page.
35. As a user, I want to define my "Target Price" for the alert.
36. As a user, I want to choose whether to receive the alert via Email or Push Notification.
37. As a system, I want to check prices daily and trigger alerts only if current price <= target price.
38. As a user, I want an email containing a direct link to the merchant when my alert triggers.
39. As a user, I want to view all my active price alerts in my account dashboard.
40. As a user, I want to edit the target price of an existing alert.
41. As a user, I want to pause or delete a price alert.
42. As a user, I want to be notified if a product on my alert list goes permanently out of stock.
43. As a guest, I want to be prompted to log in/signup when I try to set an alert.
44. As a user, I want a "Predictive Drop" hint based on historical data (e.g., "Usually drops in October").
45. As a user, I want to receive an alert if a massive coupon becomes available, even if the base price hasn't dropped.

## Epic 4: Coupons & Monetization (46-55)
46. As a shopper, I want to see a list of applicable bank offers (e.g., HDFC 10% off).
47. As a shopper, I want a "Copy Code" button for promo codes so I can easily paste it at checkout.
48. As a shopper, I want to know if a coupon has an expiration date.
49. As a platform owner, I want every merchant link to automatically include my affiliate tag.
50. As a platform owner, I want all out-clicks to route through a tracking endpoint for analytics.
51. As a user, I want a clear transition screen saying "Redirecting to store" so I understand what's happening.
52. As a platform owner, I want to track which coupons generate the most clicks.
53. As a platform owner, I want to ensure affiliate links open in a new browser tab.
54. As a shopper, I want to see hidden/exclusive deals curated by ShopSense.
55. As a platform owner, I want to tag specific links as "Sponsored" for transparency.

## Epic 5: AI Assistant (56-65)
56. As a shopper, I want a floating "Ask AI" button on product pages.
57. As a shopper, I want the AI to know which product I am currently viewing without me typing its name.
58. As a shopper, I want to ask "Is this good for gaming?" and get a context-aware answer.
59. As a shopper, I want the AI to suggest three alternative products if I ask for them.
60. As a shopper, I want the AI chat to maintain conversation history during my session.
61. As a shopper, I want the AI to warn me if the product is outdated (e.g., "A newer model exists").
62. As a system, I want to limit the AI chat to shopping-related queries to prevent abuse.
63. As a shopper, I want the AI to provide a direct link to recommended products in the chat.
64. As a shopper, I want the AI to summarize the pros and cons in bullet points.
65. As a system, I want to fall back gracefully if the LLM API times out.

## Epic 6: User Authentication & Profile (66-75)
66. As a user, I want to sign up using my Email and a secure password.
67. As a user, I want to sign up quickly using Google OAuth.
68. As a user, I want to log in and stay authenticated securely via JWT.
69. As a user, I want to reset my password via an email link if I forget it.
70. As a user, I want to update my profile name and avatar.
71. As a user, I want to toggle between Dark Mode and Light Mode in settings.
72. As a user, I want to view my recent search history so I can resume my research.
73. As a user, I want to save items to a "Wishlist" without setting a specific price alert.
74. As a user, I want to delete my account and all associated data permanently.
75. As a user, I want to manage my email notification preferences (opt-out of marketing emails).

## Epic 7: Blogs & SEO (76-85)
76. As a reader, I want to view a cleanly formatted buying guide with large typography.
77. As a reader, I want to click on products mentioned in the blog to view their live prices.
78. As an SEO specialist, I want the blog URLs to be human-readable (e.g., `/blog/best-laptops-2026`).
79. As a system, I want to automatically generate a `sitemap.xml` including all products and blogs.
80. As a system, I want to generate dynamic Open Graph tags so links look good when shared on Twitter/Facebook.
81. As a reader, I want a Table of Contents in long blog posts for easy navigation.
82. As a reader, I want to see the "Last Updated" date on guides to ensure relevancy.
83. As an admin, I want a Markdown editor to draft and publish blog posts.
84. As an admin, I want to assign SEO meta descriptions to every blog post.
85. As a system, I want all pages to have a canonical URL tag to prevent duplicate content penalties.

## Epic 8: Administration & Analytics (86-95)
86. As an admin, I want a secure dashboard accessible only to superusers.
87. As an admin, I want to see a chart of Daily Active Users (DAU).
88. As an admin, I want to see total affiliate clicks generated today.
89. As an admin, I want to manually trigger a data sync with a merchant API.
90. As an admin, I want to view a log of failed API ingestions to debug data issues.
91. As an admin, I want to ban a user account if malicious activity is detected.
92. As an admin, I want to update the platform's global alert banner (e.g., "Big Billion Days are Live!").
93. As an admin, I want to manage categories and mapping logic.
94. As an admin, I want to upload static CSV feeds for merchants without APIs.
95. As an admin, I want to monitor the queue size of Celery tasks (e.g., pending price alert emails).

## Epic 9: Non-Functional & Edge Cases (96-100)
96. As a user, I want the website to load in under 2 seconds even on a 3G mobile network.
97. As a visually impaired user, I want to navigate the site using a screen reader and keyboard tab keys.
98. As a user, I want to see a helpful 404 error page with a search bar if I visit a broken link.
99. As a user, I want the app to show a "No internet connection" banner if my Wi-Fi drops.
100. As a user, I want a clean empty state graphic when my Wishlist has no items.
