# Business Flow

This document explains the internal mechanisms, data logic, and monetization strategies of ShopSense AI.

## 1. How Products Appear (Data Ingestion)
- **Authorized Sources:** We utilize official affiliate APIs (Amazon Product Advertising API, Flipkart Affiliate API, Croma, etc.) and authorized merchant data feeds (CSV/XML).
- **Normalization:** A backend microservice normalizes incoming data (e.g., matching "Apple iPhone 15" from Amazon with "iPhone 15 128GB" from Flipkart) using AI/NLP grouping.
- **Storage:** Normalized products are stored in PostgreSQL, with search indexes pushed to Elasticsearch/Typesense for instant querying.

## 2. How Users Search
- **Search Engine:** User queries are parsed by an intelligent search layer.
- **Intent Recognition:** If a user types "cheap phones with good camera", the NLP engine translates "cheap" to a price filter (< ₹15,000) and "good camera" to a spec filter (Camera Rating > 4/5).
- **Ranking:** Results are ranked based on relevance, popularity, and availability of deals.

## 3. How Recommendations Work
- **Collaborative Filtering:** "Users who compared X also compared Y."
- **Content-Based:** Recommending products with similar specifications within the same price bracket.
- **AI-Curated:** The AI periodically generates dynamic collections (e.g., "Trending Today", "Massive Price Drops").

## 4. How Affiliate Links are Handled
- **Link Generation:** When a merchant URL is requested, the backend dynamically appends the ShopSense affiliate tag (`?tag=shopsense-21`).
- **Redirection:** The user clicks a button, hitting a ShopSense endpoint (e.g., `/out?id=123`). The server logs the click (timestamp, user ID, product ID) and issues an HTTP 302 redirect to the final affiliate URL.
- **Compliance:** Full transparency is maintained. No cloaking or misleading UI.

## 5. How Analytics are Recorded
- **Privacy-First Tracking:** Internal analytics track search queries, click-through rates (CTR), and bounce rates without selling PII (Personally Identifiable Information).
- **Conversion Tracking:** Post-back URLs or affiliate dashboard reports are imported to match outbound clicks with successful sales, calculating ROI and revenue per user.

## 6. How AI Assists Users
- **The Chatbot Layer:** Powered by a selected LLM (e.g., Gemini/OpenAI). It has read-only access to the ShopSense product database via function calling (RAG - Retrieval-Augmented Generation).
- **Contextual Awareness:** The AI knows what product page the user is currently viewing and can answer specific questions based on the product's specs and reviews.

## 7. How Notifications Work
- **Price Alerts:** A background Celery worker runs daily/hourly to check current prices against user-set target prices.
- **Trigger:** If `current_price <= target_price`, a notification payload is pushed to an email service (SendGrid/AWS SES) and/or Web Push Notification service.

## 8. How Blogs Generate Traffic (SEO Strategy)
- **Programmatic SEO:** Auto-generating pages like "Compare iPhone 15 vs Galaxy S24" based on database specs.
- **Editorial Content:** High-quality buying guides written by experts and assisted by AI, targeting long-tail keywords (e.g., "Best laptops for coding in Python under 60k").
- **Internal Linking:** Blogs seamlessly link to ShopSense product pages, trapping organic traffic into the conversion funnel.

## 9. How Revenue is Generated
- **Primary:** Affiliate commissions (CPA - Cost Per Action) ranging from 1% to 10% depending on the product category.
- **Secondary (Future):** Sponsored listings (clearly marked as "Sponsored") by brands—not merchants—wanting visibility on the platform.

## 10. Future Premium Membership (ShopSense+)
- **Concept:** A subscription model (e.g., ₹49/month).
- **Perks:**
  - Ad-free experience (if ads are ever introduced).
  - Faster, real-time price drop SMS alerts (priority queue).
  - Advanced historical price data (5-year charts instead of 1-year).
  - Exclusive cashback or reward points on top of affiliate deals.
