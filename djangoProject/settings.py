import os
import dj_database_url
from pathlib import Path

# ساختار پایه دایرکتوری پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------
# تنظیمات امنیتی و محیطی (Environment & Security Settings)
# ----------------------

# کلید مخفی باید از طریق متغیر محیطی در Production تامین شود.
# 'os.environ.get()' برای خواندن متغیر محیطی استفاده می‌شود.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-local-development')

# در محیط Production، DEBUG باید False باشد.
# متغیر محیطی 'RENDER' برای تشخیص محیط Production استفاده می‌شود.
DEBUG = 'RENDER' not in os.environ

# آدرس‌هایی که اجازه دارند به سایت دسترسی داشته باشند.
# آدرس سایت رندر شما باید اینجا اضافه شود (مثلاً my-resume-project.onrender.com).
# در Production، '*' به Render اجازه می‌دهد تا آدرس‌ها را مدیریت کند.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ----------------------
# اپلیکیشن‌های نصب شده (Installed Applications)
# ----------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # اپلیکیشن‌های شما:
    'Home_app.apps.HomeAppConfig', 
    # 'Resume_app.apps.ResumeAppConfig', 
]

# ----------------------
# Middleware
# ----------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise باید بلافاصله پس از SecurityMiddleware قرار گیرد تا فایل‌های استاتیک را سرویس دهد
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

# ----------------------
# تنظیمات Template
# ----------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # دایرکتوری مرکزی تمپلیت
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# ----------------------
# تنظیمات دیتابیس (Database Configuration)
# ----------------------

if 'DATABASE_URL' in os.environ:
    # استفاده از dj_database_url برای اتصال به PostgreSQL در Production (Render)
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # تنظیمات دیتابیس پیش‌فرض برای SQLite در محیط Local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ----------------------
# تنظیمات احراز هویت و اعتبارسنجی (Auth & Validation)
# ----------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# ----------------------
# تنظیمات بین‌المللی (Internationalization)
# ----------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ----------------------
# تنظیمات Static Files (برای رفع خطای logo.png)
# ----------------------

# 1. مسیر دایرکتوری‌های استاتیک در Development 
# این لیست به جنگو می‌گوید علاوه بر پوشه‌های 'static' داخل اپلیکیشن‌ها، کجا به دنبال فایل بگردد.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 2. آدرس URL برای سرویس‌دهی
STATIC_URL = 'static/'

# 3. محلی که collectstatic فایل‌ها را در Production جمع‌آوری می‌کند (پوشه staticfiles)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 4. تنظیم WhiteNoise Storage
# (این در صورتی استفاده می‌شود که STORAGES تعریف نشده باشد، اما برای اطمینان نگه داشته می‌شود)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ----------------------
# تنظیمات امنیتی اضافه برای Production (Render)
# ----------------------

if not DEBUG:
    # اجبار به استفاده از HTTPS (برای Production)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # فشرده‌سازی فایل‌های استاتیک در Production با WhiteNoise
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
            # **** مهم: تنظیم manifest_strict: False برای نادیده گرفتن فایل‌های گم‌شده (مانند .map) ****
            "OPTIONS": {
                "manifest_strict": False,
            }
        },
    }

# ----------------------
# متغیر MEDIA (اگر دارید)
# ----------------------

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------
# تنظیمات WhiteNoise (برای رفع خطای Source Map در Production)
# توجه: تنظیم WHITENOISE_ALLOW_INSECURE_CONTENT حذف شد زیرا برای این خطا کار نمی‌کرد.
# این تنظیم WHITENOISE_MANIFEST_HASSING به طور خودکار توسط STATICFILES_STORAGE کنترل می‌شود.
WHITENOISE_MANIFEST_HASSING = True