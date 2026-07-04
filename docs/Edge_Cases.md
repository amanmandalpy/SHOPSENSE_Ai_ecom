# Edge Cases & QA Scenarios

This document outlines critical edge cases and how the ShopSense AI system should handle them to ensure a robust user experience.

## 1. Search & Discovery
- **No Search Results:** Display a friendly message ("We couldn't find exactly that, but check these out...") and show a grid of trending products or related categories instead of a blank page.
- **Typo Extreme:** If a user types gibberish (e.g., "asdfgh"), gracefully return 0 results and suggest checking spelling.
- **Special Characters:** Strip out SQL injection attempts (`' OR 1=1`) or script tags via strict input sanitization; process the remaining alphanumeric string.

## 2. Product Data & Affiliate Links
- **Merchant Out of Stock:** The platform should query live API endpoints (or rely on cached data < 1hr old). If out of stock, gray out the "Go to Store" button and label it "Out of Stock".
- **Affiliate Link Expired/Broken:** If the affiliate redirect fails, the system logs a `500` internally but redirects the user to the merchant's generic homepage so the journey doesn't entirely break.
- **Price Changed at Merchant:** If a user clicks a ₹500 product, but the merchant site says ₹600 (due to caching delay), ShopSense must display a disclaimer on the PDP: *"Prices are subject to change based on merchant updates."*
- **Image Missing/Broken:** Implement a fallback `placeholder_image.webp` (with a generic box icon) via the `onError` attribute on `<img>` tags.

## 3. Alerts & Notifications
- **Notification Failure (Email Bounce):** If SendGrid returns a bounce, flag the user's email as invalid in the DB and stop attempting to send future alerts to save API costs.
- **Unrealistic Target Price:** If a user sets an alert for ₹1 on a ₹1,00,000 laptop, the system accepts it but never triggers. (Alternatively, add a validation rule: Target price cannot be < 10% of current price).
- **Timezone Issues:** Ensure all Cron jobs run on UTC, but display timestamps to users in IST (Indian Standard Time).

## 4. User Accounts & Infrastructure
- **User Deletes Account:** Hard delete all PII (Email, Name). Soft delete or anonymize tracking data (e.g., change user_id to 'anonymous' in analytics tables) to preserve system metrics.
- **Server/DB Slowdown:** Implement circuit breakers. If the DB takes > 3s to respond, return cached homepage data or a polite "We are experiencing high traffic, please try again" page.
- **Internet Lost:** Service Worker (PWA feature) should intercept requests and show a custom offline page instead of the browser's dinosaur game.

## 5. AI Assistant
- **AI Not Available / API Rate Limit:** If the LLM provider is down, hide the "Ask AI" button entirely or display a toast: *"Our AI is currently resting. Please check specs manually."*
- **AI Hallucinations:** Use strict system prompts and low temperature settings. Instruct the AI to say *"I do not have that information"* if the data isn't in the provided context, preventing it from inventing fake features or prices.
- **Inappropriate Queries:** The AI must block non-shopping questions (e.g., politics, coding) gracefully: *"I am an AI Shopping Assistant. I can only help you with product comparisons and deals!"*
