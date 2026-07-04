# ShopSense AI v1.0

ShopSense AI is a next-generation e-commerce comparison engine powered by Gemini AI.

## Architecture Highlights
- **Django 5.1 & Python 3.13**: Secure, robust backend.
- **Celery & Redis**: Background processing for AI jobs, Price Alerts, and email queues.
- **Business Operating System (BOS)**: Complete custom admin panel overriding standard Django Admin.
- **Tailwind CSS**: Utility-first CSS framework for rapid and beautiful UI.

## Modules
1. **Core / Accounts**: Custom User model, auth flows, personalized dashboard.
2. **Products / Categories**: Taxonomy engine, specifications, variants.
3. **Price Tracking & Alerts**: Automated Celery workers monitoring merchant price drops.
4. **AI Assistant**: Gemini integration for contextual buying guides and product recommendations.
5. **Coupons / Offers**: Deal engine.
6. **Support / Legal**: Centralized FAQ and compliance engine.
7. **BOS / Analytics**: Real-time traffic, ticket, and sales dashboard.

For deployment instructions, please see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).
