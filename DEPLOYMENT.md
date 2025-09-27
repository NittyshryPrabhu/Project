# Deployment guide — withfamily

This document provides a concise path to deploy the Django "withfamily" app to an Ubuntu server (tested concepts on Ubuntu 22.04). It assumes you have sudo access.

1) Create a system user and directory

   sudo adduser --disabled-password --gecos '' youruser
   sudo mkdir -p /home/youruser/withfamily
   sudo chown youruser:youruser /home/youruser/withfamily

2) Install system packages

   sudo apt update
   sudo apt install python3 python3-venv python3-pip nginx git postgresql postgresql-contrib

3) Create Postgres DB & user

   sudo -u postgres psql
   CREATE DATABASE withfamily_db;
   CREATE USER withfamily_user WITH PASSWORD 'strongpassword';
   GRANT ALL PRIVILEGES ON DATABASE withfamily_db TO withfamily_user;
   \q

4) Clone repo and create virtualenv

   git clone <repo-url> /home/youruser/withfamily
   cd /home/youruser/withfamily
   python3 -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt

5) Environment variables

   cp .env.example .env
   # Edit .env: set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DATABASE_URL (postgres url)

6) Collect static, apply migrations

   . venv/bin/activate
   python manage.py migrate
   python manage.py collectstatic --noinput

7) Create systemd service and start it

   sudo cp deploy/withfamily.service /etc/systemd/system/withfamily.service
   sudo systemctl daemon-reload
   sudo systemctl start withfamily
   sudo systemctl enable withfamily

8) Nginx

   sudo cp deploy/withfamily.nginx /etc/nginx/sites-available/withfamily
   sudo ln -s /etc/nginx/sites-available/withfamily /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx

9) Optional: configure HTTPS with certbot

   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

10) Create admin user

   . venv/bin/activate
   python manage.py createsuperuser

That's it — the app should be live. If you need a Docker-based deployment or Azure/GCP/Heroku recipe, tell me which target and I will add it.
