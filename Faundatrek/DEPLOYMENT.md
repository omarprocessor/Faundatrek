# FaundaTrek Backend - Deployment Guide

This guide covers deploying the FaundaTrek Django backend to various cloud platforms.

## 🚀 Quick Deployment Options

### 1. Railway (Recommended for Beginners)

Railway is the easiest way to deploy Django apps with automatic PostgreSQL setup.

**Steps:**
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub repository
4. Railway will auto-detect Django and set up the environment
5. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://... (auto-provided by Railway)
   ALLOWED_HOSTS=.railway.app
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

### 2. Heroku

**Prerequisites:**
- Heroku CLI installed
- Git repository

**Steps:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-fundatrek-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ALLOWED_HOSTS=.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### 3. AWS (Production Ready)

**Services Used:**
- **RDS**: PostgreSQL database
- **S3**: File storage
- **EC2**: Application server
- **Route 53**: Domain management
- **CloudFront**: CDN

**Steps:**
1. Launch EC2 instance (Ubuntu recommended)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```
3. Set up PostgreSQL on RDS
4. Configure S3 for file storage
5. Set up Nginx as reverse proxy
6. Use Gunicorn as WSGI server
7. Set up SSL with Let's Encrypt

### 4. DigitalOcean

**App Platform (Easiest):**
1. Connect GitHub repository
2. Choose Django framework
3. Add environment variables
4. Deploy with one click

**Droplet (More Control):**
1. Create Ubuntu droplet
2. Follow similar steps as AWS EC2
3. Use Spaces for file storage

## 🔧 Environment Configuration

### Production Environment Variables

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=fundatrek_prod
DB_USER=fundatrek_user
DB_PASSWORD=secure-password
DB_HOST=your-db-host
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=7

# File Storage (AWS S3)
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=your-cdn-domain.com

# CORS Settings
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ALLOW_CREDENTIALS=True

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

## 📊 Database Setup

### PostgreSQL (Production)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE fundatrek_prod;
CREATE USER fundatrek_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE fundatrek_prod TO fundatrek_user;
\q

# Update Django settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fundatrek_prod',
        'USER': 'fundatrek_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### SQLite (Development Only)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🗄️ File Storage Configuration

### Local Storage (Development)

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### AWS S3 (Production)

```bash
pip install django-storages boto3
```

```python
# settings.py
USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    
    # S3 Static and Media files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # S3 Object Parameters
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # S3 Bucket Auth
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_QUERYSTRING_AUTH = False
```

## 🔒 Security Configuration

### Production Security Settings

```python
# settings.py

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS Security
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]

# JWT Security
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_SECRET_KEY'),
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

## 🚀 WSGI Server Configuration

### Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Create gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
```

### Systemd Service (Linux)

```ini
# /etc/systemd/system/fundatrek.service
[Unit]
Description=FaundaTrek Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fundatrek
Environment="PATH=/var/www/fundatrek/venv/bin"
ExecStart=/var/www/fundatrek/venv/bin/gunicorn --config gunicorn.conf.py fundatrek_backend.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🌐 Nginx Configuration

```nginx
# /etc/nginx/sites-available/fundatrek
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static files
    location /static/ {
        alias /var/www/fundatrek/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/fundatrek/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Django app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📱 Frontend Integration

### CORS Configuration

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "http://localhost:3000",  # Development
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### API Base URL

```javascript
// Frontend configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com/api'
  : 'http://localhost:8000/api';
```

## 🔍 Monitoring & Logging

### Django Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/fundatrek/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Check Endpoint

```python
# views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)
```

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Media files configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Domain DNS configured
- [ ] Frontend CORS settings updated
- [ ] Load testing completed
- [ ] Documentation updated

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database credentials
   - Verify network connectivity
   - Check firewall settings

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check Nginx configuration
   - Verify file permissions

3. **CORS Errors**
   - Check CORS_ALLOWED_ORIGINS
   - Verify frontend domain
   - Check browser console for errors

4. **JWT Token Issues**
   - Verify JWT_SECRET_KEY
   - Check token expiration
   - Verify Authorization header format

### Useful Commands

```bash
# Check Django status
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Check static files
python manage.py collectstatic --dry-run

# Monitor logs
tail -f /var/log/fundatrek/django.log

# Check Nginx status
sudo systemctl status nginx

# Check Gunicorn status
sudo systemctl status fundatrek
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/docs/)
- [AWS Documentation](https://aws.amazon.com/documentation/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
