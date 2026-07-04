# Affiliate Tracking Guide

Welcome to the ShopSense AI Affiliate Tracking Engine. This engine is responsible for transparently logging clicks out of the platform while safely applying merchant tracking identifiers and parameters.

## Core Flow
1. User clicks a "Buy Now" button.
2. The user is sent to `/out/<merchant_product_id>/`.
3. `AffiliateRedirectService` resolves the `MerchantProduct`, checks if the merchant is active, and fetches the corresponding `AffiliateAccount`.
4. Relevant tracking parameters are dynamically appended based on merchant rules (e.g., `tag` for Amazon, `affid` for Flipkart).
5. We parse the request `User-Agent`, `IP Address`, and `Session` and save it to `AffiliateClick`.
6. A HTTP 302 Found redirect is issued.

## Analytics Aggregation
Clicks are collected individually in `tracking_affiliateclick`. However, for fast dashboards, this data is periodically rolled up:
- **ProductAnalytics**: Aggregates `views_count` and `affiliate_clicks` to compute a `ctr` (Click Through Rate). 
- **MerchantAnalytics**: Daily summaries mapping the total and unique clicks outbound to a specific merchant.

## Using Celery
Ensure your Celery beat is running. It will execute:
- `aggregate_daily_analytics`: Rolls up yesterday's clicks to merchants.
- `calculate_product_ctrs`: Periodically sweeps product views and clicks to maintain accurate CTR metrics across the catalog.
