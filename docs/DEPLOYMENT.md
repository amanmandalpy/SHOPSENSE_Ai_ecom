# ShopSense AI - Deployment Guide

This guide outlines the steps required to deploy ShopSense AI Version 1.0 to an AWS Ubuntu environment.

## 1. Prerequisites
- **AWS EC2 Instance**: Ubuntu 24.04 LTS recommended.
- **PostgreSQL Database**: Amazon RDS or local PostgreSQL.
- **Redis**: Amazon ElastiCache or local Redis server.
- **AWS S3 Bucket**: For media and static files.

## 2. Server Setup

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis-server supervisor -y
```

## 3. Clone and Setup Environment

```bash
git clone https://github.com/yourrepo/shopsense-ai.git
cd shopsense-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Environment Variables
Copy the example environment file and update with production credentials.
```bash
cp deploy/.env.example .env
```

## 5. Database & Static Files
```bash
export DJANGO_SETTINGS_MODULE="shopsense.settings.prod"
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

## 6. Configure Services

### Gunicorn
Copy the systemd service file:
```bash
sudo cp deploy/gunicorn/gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Nginx
Configure the reverse proxy:
```bash
sudo cp deploy/nginx/shopsense.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/shopsense.conf /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Supervisor (Celery)
Set up the Celery background worker:
```bash
sudo cp deploy/supervisor/celery.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start celery
```

## 7. Security (Let's Encrypt SSL)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d shopsense.com -d www.shopsense.com
```

Your application is now deployed and running on `https://shopsense.com`.
