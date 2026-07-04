# AWS Deployment Guide

ShopSense AI is designed to run on a standard AWS stack: EC2 (App/Celery), RDS (PostgreSQL), ElastiCache (Redis), and S3 (Media/Static).

## 1. Infrastructure Provisioning
1. **RDS:** Spin up a PostgreSQL 15 instance. Keep it in a private subnet.
2. **ElastiCache:** Spin up a Redis node.
3. **S3:** Create an S3 bucket (e.g., `shopsense-assets-prod`). Disable "Block all public access" and attach an IAM policy for your EC2 instance profile.
4. **EC2:** Launch an Ubuntu 22.04 LTS instance.

## 2. Server Configuration (EC2)
SSH into your instance and install dependencies:
```bash
sudo apt update
sudo apt install python3.11-venv postgresql-client nginx supervisor redis-server
```

Clone the repository to `/var/www/shopsense`.

## 3. Environment Variables
Create `/var/www/shopsense/.env`:
```
DJANGO_SETTINGS_MODULE=shopsense.settings.prod
SECRET_KEY=your_secure_random_string
ALLOWED_HOSTS=shopsense.ai,www.shopsense.ai
DB_NAME=shopsense
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your-rds-endpoint.amazonaws.com
REDIS_URL=redis://your-elasticache-endpoint:6379/1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=shopsense-assets-prod
GROQ_API_KEY=...
```

## 4. Run Migrations & Collect Static
```bash
cd /var/www/shopsense
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## 5. Supervisor (Gunicorn & Celery)
Link the provided Gunicorn config to supervisor, or run it directly:
`gunicorn shopsense.wsgi:application -c infrastructure/gunicorn_config.py`

Start Celery:
`celery -A shopsense worker -l INFO`

## 6. Nginx & SSL
Copy `infrastructure/nginx.conf` to `/etc/nginx/sites-available/shopsense`.
Symlink it to `sites-enabled`.
Run Certbot:
`sudo certbot --nginx -d shopsense.ai -d www.shopsense.ai`
