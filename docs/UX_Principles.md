# UX & Error Handling Principles

This document defines the core user experience philosophy and how the system should handle errors gracefully.

## 1. Core UX Philosophy
- **Minimal:** Remove all unnecessary borders, lines, and text. Let the product images and data breathe. Use whitespace (negative space) as a structural element.
- **Premium:** Utilize soft shadows, rounded corners (`border-radius`), and smooth bezier-curve micro-animations (e.g., button hover states lifting slightly).
- **Fast:** Users perceive speed through UI. Use skeleton loaders instead of spinning wheels. Render layout instantly.
- **Trustworthy:** Never hide fees. Clearly state when users are leaving the site. Display accurate data. No clickbait UI.
- **Secure:** Indicate security where it matters (e.g., lock icons on login forms).

## 2. Error Handling Philosophy
Errors happen, but they should never break the user's trust or momentum.

### What Users Should See
- **Human-Readable Text:** Never display technical stack traces or database errors to the user (e.g., "Error 500: Database Connection Refused").
- **Actionable Advice:** Instead, say "Oops, our servers are taking a quick break. Please try refreshing the page." Provide a clear action (e.g., a "Retry" or "Go Home" button).
- **Contextual Errors:** If a specific component fails (e.g., Price History chart doesn't load), do not crash the whole page. Display an error state locally within that card ("Chart data unavailable right now"), while the rest of the product page remains fully usable.

### What Should Be Logged
- **Detailed Traces:** All exceptions, stack traces, request payloads (excluding passwords/PII), and timestamps must be logged to a centralized service (e.g., Sentry, Datadog, AWS CloudWatch).
- **Severity Levels:** Classify logs correctly (INFO, WARN, ERROR, CRITICAL) to trigger appropriate developer alerts.

### What Should Be Retried
- **Idempotent Operations:** Network timeouts for read-only actions (like searching or fetching a product) should be automatically retried 2-3 times by the Axios/Fetch client under the hood before showing an error to the user.
- **Third-Party APIs:** If an affiliate API fails to return the price, implement exponential backoff on the backend.

### Graceful Degradation
- If the Redis cache goes down, the backend should fall back to querying PostgreSQL directly (slower, but functional).
- If JavaScript fails to load on the frontend, the core site should still be navigable (Semantic HTML links still work), ensuring the user isn't trapped on a blank white screen.
