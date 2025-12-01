import os
import dj_database_url
from pathlib import Path
# ایمپورت کردن کلاس پایه از WhiteNoise
from whitenoise.storage import CompressedManifestStaticFilesStorage

# --- کلاس سفارشی WhiteNoise Storage ---
# این کلاس، ویژگی manifest_strict را روی False تنظیم می‌کند تا خطاهای مربوط به
# فایل‌های Source Map (.map) که اغلب در محیط Production موجود نیستند، نادیده گرفته شوند.
class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False
# ---------------------------------------


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
    'contact_app', 
    'my_team', # <--- اپلیکیشن my_team اضافه شد
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
# تنظیمات Static Files 
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

# ----------------------
# تنظیمات امنیتی اضافه برای Production (Render)
# ----------------------

if not DEBUG:
    # اجبار به استفاده از HTTPS (برای Production)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # 4. تنظیم WhiteNoise Storage برای Production
    # استفاده از کلاس سفارشی WhiteNoiseStaticFilesStorage (که در بالای همین فایل تعریف شده)
    # برای اطمینان از نادیده گرفتن خطای Source Map.
    STATICFILES_STORAGE = 'djangoProject.settings.WhiteNoiseStaticFilesStorage'
    
    # متغیر محیطی WHITENOISE_MANIFEST_STRICT دیگر مورد نیاز نیست.