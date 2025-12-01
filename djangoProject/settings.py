# djangoProject/settings.py
# -----------------------------------------------------

from pathlib import Path
import os
import dj_database_url # مدیریت آسان اتصال دیتابیس از طریق URL

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ۱. تنظیمات امنیتی ضروری برای Production
# ==========================================================

# SECRET_KEY: از متغیر محیطی بخوانید. از مقدار جایگزین فقط برای محیط توسعه لوکال استفاده کنید.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-2=#49=b%(inur)!ev+ys^5f6v$m=le9by)e4_du148e_gy28av')

# DEBUG: در محیط سرور باید False باشد.
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
    
    # WhiteNoise باید مستقیماً بعد از SecurityMiddleware باشد.
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# ==========================================================
# ۳. تنظیمات دیتابیس (پشتیبانی از SQLite و Postgres)
# ==========================================================

# اگر متغیر محیطی DATABASE_URL (توسط Render) وجود داشت، از Postgres استفاده کن.
if os.environ.get('DATABASE_URL'):
    # تنظیمات دیتابیس Render (PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  # تنظیمات برای اتصال پایدار
        )
    }
else:
    # در غیر این صورت (برای محیط لوکال)، از SQLite استفاده کن.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================================================
# ۴. سایر تنظیمات
# ==========================================================

# ... (بخش AUTH_PASSWORD_VALIDATORS، LANGUAGE_CODE و TIME_ZONE بدون تغییر)
# (توجه: من این بخش ها را در کد نهایی حذف کردم اما شما باید در فایل خود نگه دارید)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# ۵. تنظیمات Static & Media Files
# ==========================================================

STATIC_URL = '/static/'

# مسیری برای جمع‌آوری فایل‌های استاتیک در Production (توسط collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'assets'),
]

# تنظیمات WhiteNoise برای فشرده‌سازی و کش کردن فایل‌های Static
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media Files (توجه: برای Production باید از S3 یا مشابه استفاده شود)
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")