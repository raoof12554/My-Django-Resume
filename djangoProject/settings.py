from pathlib import Path
import os
import dj_database_url
from decouple import config 

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ۱. تنظیمات امنیتی و محیط Production
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-2=#49=b%(inur)!ev+ys^5f6v$m=le9by)e4_du148e_gy28av')
DEBUG = os.environ.get('DEBUG') == 'True' 

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ==========================================================
# ۲. App ها و Middleware ها
# ==========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # اضافه کردن django-storages برای مدیریت فضای ابری S3
    'storages',
    
    'Home_app',
    'contact_app',
    'my_team',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

# ==========================================================
# ۳. TEMPLATES 
# ==========================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# ==========================================================
# ۴. تنظیمات دیتابیس
# ==========================================================
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600 
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================================================
# ۵. سایر تنظیمات
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# ۶. تنظیمات Static & Media Files
# ==========================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'assets',
]

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = BASE_DIR / "mediafiles"

# پیکربندی مدرن ذخیره‌سازی فایل‌ها (Django 4.0+)
STORAGES = {
    # پیکربندی Static File Storage توسط WhiteNoise
    "staticfiles": {
        # تغییر به WhiteNoiseStaticFilesStorage ساده‌تر برای حل خطای Post-processing
        # این بک‌اند از Manifest و Hashing برای امنیت استفاده می‌کند اما گام Compression را حذف می‌کند 
        # و در یافتن فایل‌های جانبی مثل map.files کمتر سختگیر است.
        "BACKEND": "whitenoise.storage.WhiteNoiseStaticFilesStorage",
    },
    
    # *** پیکربندی Media File Storage برای Production (S3) ***
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Storage"
        if not DEBUG else "django.core.files.storage.FileSystemStorage",
    },
}

# ==========================================================
# ۷. تنظیمات S3/Boto3 (فقط در Production استفاده می‌شود)
# ==========================================================
# این متغیرها باید در Render به عنوان متغیرهای محیطی (Environment Variables) تنظیم شوند.

if not DEBUG:
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = 'media' 
    
    AWS_S3_REGION_NAME = os.environ.get('AWS_REGION', 'us-east-1') 
    AWS_DEFAULT_ACL = 'public-read' 

    if not AWS_S3_CUSTOM_DOMAIN:
        AWS_S3_CUSTOM_DOMAIN = f'{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
    

# ==========================================================
# ۸. تنظیمات WhiteNoise (رفع خطای MissingFileError)
# ==========================================================
WHITENOISE_IGNORE_FILE_TYPES = ['map', 'eot', 'ttf', 'woff', 'woff2', 'otf']
WHITENOISE_MANIFEST_STRICT = False

# **تنظیم WHITENOISE_SKIP_COMPRESS_CONTENT حذف شد** # و با تغییر WhiteNoiseStaticFilesStorage جایگزین شد.


# ==========================================================
# ۹. متغیرهای سفارشی 
# ==========================================================
RESUME_NAME = os.environ.get('RESUME_NAME', 'رزومه خورشید ریانه (نسخه لوکال)')