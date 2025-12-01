from pathlib import Path
import os
import dj_database_url
# config از decouple در محیط Production توسط os.environ جایگزین می‌شود، اما برای لوکال نگهداری می‌شود.
from decouple import config 

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ۱. تنظیمات امنیتی و محیط Production
# ==========================================================

# SECRET_KEY: خواندن از متغیر محیطی (ضروری در Render)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-2=#49=b%(inur)!ev+ys^5f6v$m=le9by)e4_du148e_gy28av')

# DEBUG: در Render (Production) باید False باشد مگر اینکه صریحاً True تنظیم شده باشد.
# اگر متغیر محیطی DEBUG تنظیم نشده باشد، پیش‌فرض False است.
DEBUG = os.environ.get('DEBUG') == 'True' 

# ALLOWED_HOSTS: آدرس های مجاز برای دسترسی به سایت
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

# اضافه کردن آدرس Render به لیست میزبان‌های مجاز
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ==========================================================
# ۲. App ها و Middleware ها
# ==========================================================

INSTALLED_APPS = [
    # هسته Django
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
    
    # WhiteNoise برای مدیریت فایل‌های استاتیک در Production - باید بلافاصله بعد از SecurityMiddleware باشد
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
# ۳. TEMPLATES (تنظیمات نهایی برای رفع خطای admin.E403)
# ==========================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # استفاده از pathlib.Path برای مسیردهی تمپلیت‌های اصلی
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # این دو خط برای عملکرد Admin و Static/Media ضروری هستند
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# ==========================================================
# ۴. تنظیمات دیتابیس (پشتیبانی از SQLite و Postgres)
# ==========================================================

# در Render از DATABASE_URL (Postgres) و در لوکال از SQLite استفاده می‌شود.
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

# تنظیمات زبان و زمان
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# ۶. تنظیمات Static & Media Files (با استفاده از STORAGES)
# ==========================================================

STATIC_URL = '/static/'

# مسیری برای جمع‌آوری فایل‌های استاتیک در Production (توسط collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# دایرکتوری‌های حاوی فایل‌های استاتیک که در اپ‌ها نیستند
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'assets',
]

# Media Files (فایل‌های آپلود شده توسط کاربر)
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = BASE_DIR / "mediafiles"

# پیکربندی مدرن ذخیره‌سازی فایل‌ها (Django 4.0+)
STORAGES = {
    # Default file storage (برای فایل‌های Media)
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # Static file storage (برای WhiteNoise)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==========================================================
# ۷. تنظیمات WhiteNoise (رفع خطای MissingFileError)
# ==========================================================

# WhiteNoise را برای نادیده گرفتن فایل‌های Map و فونت که در Production مورد نیاز نیستند، تنظیم می‌کند.
# این تنظیم خطای whitenoise.storage.MissingFileError را رفع می‌کند.
WHITENOISE_IGNORE_FILE_TYPES = ['map', 'eot', 'ttf', 'woff', 'woff2', 'otf']

# اجبار WhiteNoise برای صدور هشدار به جای خطای بحرانی اگر فایل‌های ارجاع داده شده پیدا نشوند.
# این اغلب مشکل فایل‌های Map را که به طور کامل توسط ignore_file_types حذف نمی‌شوند، حل می‌کند.
WHITENOISE_MANIFEST_STRICT = False


# ==========================================================
# ۸. متغیرهای سفارشی 
# ==========================================================

RESUME_NAME = os.environ.get('RESUME_NAME', 'رزومه خورشید ریانه (نسخه لوکال)')