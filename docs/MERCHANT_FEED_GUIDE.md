# Merchant Feed Guide

Welcome to the ShopSense AI Merchant Feed Engine. This guide provides information on how to configure and onboard a new merchant feed.

## Supported Feed Types
- **CSV**: Standard comma-separated values.
- **JSON**: JSON files (preferably array of objects).
- **XML**: XML feeds.

## Configuring a Feed
1. Navigate to the **Django Admin** -> **Merchant Feeds**.
2. Click **Add Merchant Feed**.
3. Select the associated **Merchant** (e.g. Amazon).
4. Provide a descriptive **Name**.
5. Select the **Feed Type** and input the **Feed URL**.
6. Set the **Auth Type** if the feed requires basic auth or API keys.
7. Set the **Sync Frequency** in minutes (default is 1440 for daily sync).
8. Save as `ACTIVE`. 

## How the Sync Works
The Celery beat scheduler runs `schedule_due_feeds()` every few minutes. It finds feeds where `next_sync` is in the past, and queues an `execute_feed_import` task. 
The Import Pipeline:
1. Downloads the feed.
2. Streams and parses the feed (memory efficient).
3. Normalizes fields using heuristic mapping (e.g., mapping `current_price`, `sale_price`, `price` to our internal `price` field).
4. Detects duplicates using SKU matching.
5. Performs `bulk_create` / `bulk_update` in batches of 500.

## Troubleshooting
Check the **Merchant Sync Logs** or **Merchant Import Errors** in the admin dashboard for detailed tracebacks and exact failed JSON payloads.
