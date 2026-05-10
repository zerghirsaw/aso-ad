import os
from pathlib import Path
from dotenv import load_dotenv # Tambahkan ini

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# [ZERO-TRUST] Kredensial diambil dari Environment Variables
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '<SECRET_KEY_PROD>')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '<IP_OR_DOMAIN>').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api_gateway',
    'security_firewall',
    'core_engine_ml',
    'audit_siem',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# [UI CONFIGURATION] Dibutuhkan oleh Dashboard Admin Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'aso_ad_project.urls'

# [ZERO-TRUST] Database Audit SIEM (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', '<DB_NAME>'),
        'USER': os.environ.get('DB_USER', '<DB_USER>'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '<DB_PASS>'),
        'HOST': os.environ.get('DB_HOST', '<DB_HOST>'),
        'PORT': '5432',
    }
}

# [ZERO-TRUST] Redis Firewall (Dynamic Blackhole)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://<REDIS_IP>:6379/1'),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
    }
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

TIME_ZONE = 'UTC'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = 'static/'
