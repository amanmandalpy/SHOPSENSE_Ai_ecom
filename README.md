# ShopSense AI

ShopSense AI is a next-generation eCommerce aggregation and intelligence platform designed to help consumers find the absolute best deals across the internet using Artificial Intelligence.

## Features
- **Price Tracking:** Monitor historical price drops across multiple retailers.
- **AI Assistant:** Chat natively with an AI that knows the entire product catalog and active discounts.
- **Smart Comparison:** Instantly compare specifications side-by-side.
- **Personalization Engine:** A dynamic homepage that curates "Recommended for You" products based on your live browsing history.
- **Coupons & Savings:** Automatically calculates the absolute cheapest price after applying bank and festival offers.

## Tech Stack
- **Backend:** Django (Python 3.11)
- **Database:** PostgreSQL (AWS RDS) & Redis (AWS ElastiCache)
- **Frontend:** HTML, TailwindCSS Vanilla
- **AI Integration:** Groq (Llama-3) API
- **Infrastructure:** AWS EC2, S3, Celery, Gunicorn, Nginx

## Local Development
1. Clone the repository.
2. `python -m venv .venv` and `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill variables.
5. `python manage.py migrate`
6. `python manage.py runserver`

For deployment instructions, see `docs/DEPLOYMENT.md`.
