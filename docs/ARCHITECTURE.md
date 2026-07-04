# ShopSense AI - Architecture Summary

## 1. Data Layer
- **Products vs Merchant Products:** The platform separates a canonical `Product` (e.g. iPhone 15) from a `MerchantProduct` (e.g. iPhone 15 on Amazon). This enables true 1-to-N comparison mapping.
- **Price History:** Handled by a time-series model `PriceHistory` tied to Celery cron tasks that query merchant APIs.

## 2. Intelligence Layer
- **Savings Engine (`offers` & `coupons`):** Dynamically parses available bank offers. The `ShoppingScoreService` aggregates Base Price - Discounts + Cashback to rank items.
- **AI Assistant:** Uses the Groq API for rapid LLM inference. The Django backend injects the User's query alongside a serialized dump of active products, allowing the LLM to act as a highly intelligent Search filter.

## 3. Personalization & Analytics Layer
- **Browsing History:** Middleware logs every PDP view into a `BrowsingHistory` table (capped at 50 per user).
- **Analytics Service:** The `PlatformEvent` model uses a `JSONField` to store unstructured event metadata (like search strings or AI prompt sizes), minimizing schema bloat while allowing deep data-lake style querying in the Admin Dashboard.

## 4. Infrastructure
- Gunicorn handles WSGI HTTP requests.
- Nginx reverse proxies and serves SSL.
- `django-ratelimit` protects high-compute routes.
- Celery / Redis manages asynchronous Price Alert emails and background price scraping.
