# djangoProject/settings.py
# -----------------------------------------------------

from pathlib import Path
import os
import dj_database_url # اضافه کردن برای مدیریت دیتابیس در محیط Render (در صورت نیاز به Postgres)

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ۱. تنظیمات امنیتی ضروری برای Production
# ==========================================================

# SECRET_KEY را از متغیرهای محیطی بخوانید. در Render باید آن را تنظیم کنید.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-2=#49=b%(inur)!ev+ys^5f6v$m=le9by)e4_du148e_gy28av')

# DEBUG: در محیط سرور باید False باشد. اگر متغیر محیطی DEBUG=True باشد، آن را True می‌کند.
DEBUG = os.environ.get('DEBUG') == 'True' 

# ALLOWED_HOSTS: آدرس های مجاز برای دسترسی به سایت
# آدرس لوکال و آدرس استقرار Render را اضافه می‌کند.
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
    # App های پروژه شما
    'Home_app',
    'contact_app',
    'my_team',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # Whitenoise باید مستقیماً بعد از SecurityMiddleware باشد.
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

# ... (بخش TEMPLATES بدون تغییر)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
# ۳. تنظیمات دیتابیس (SQLite برای استقرار سریع)
# ==========================================================

# در سریع‌ترین حالت، از دیتابیس لوکال SQLite استفاده می‌کنیم.
# اگر خواستید به Postgres تغییر دهید، این بخش نیاز به تغییر دارد.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================================
# ۴. سایر تنظیمات
# ==========================================================

# ... (بخش AUTH_PASSWORD_VALIDATORS و LANGUAGE_CODE بدون تغییر)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# ۵. تنظیمات Static & Media Files
# ==========================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'assets'),
]
# مسیری که Whitenoise فایل‌های Static را از آن جمع‌آوری و سرو می‌کند.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected')
# تنظیمات Whitenoise برای فشرده‌سازی و کش کردن فایل‌های Static
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media Files: توجه داشته باشید که Render از سرویس فایل‌های آپلود شده (MEDIA_ROOT)
# بدون استفاده از سرویس‌های خارجی (مانند S3) پشتیبانی نمی‌کند.
# برای رزومه موقت، فایل‌های MEDIA شما (مانند تصاویر تیم و پروژه) باید از طریق 
# کد پروژه (یعنی در مخزن گیت‌هاب) در دسترس باشند.
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")