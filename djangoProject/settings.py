from pathlib import Path
import os
import dj_database_url
from decouple import config 
import logging
from whitenoise.storage import CompressedManifestStaticFilesStorage 
from django.core.exceptions import SuspiciousFileOperation

# تنظیم لاگر برای استفاده در کلاس سفارشی
logger = logging.getLogger(__name__)

# ==========================================================
# کلاس سفارشی برای رفع خطای Collectstatic
# ==========================================================
class CustomWhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """
    این کلاس CompressedManifestStaticFilesStorage را توسعه می‌دهد تا خطاهای 
    MissingFileError و SuspiciousFileOperation را در حین post-processing نادیده بگیرد.
    """
    
    def hashed_name(self, name, content=None):
        """
        SuspiciousFileOperation را در حین تلاش برای پیدا کردن فایل‌های ارجاع داده شده نادیده می‌گیرد.
        این خطا معمولاً به دلیل مسیرهای نسبی است که به بیرون از STATIC_ROOT اشاره می‌کنند.
        """
        try:
            # اجرای منطق استاندارد هشینگ (ManifestStaticFilesStorage)
            return super().hashed_name(name, content)
        except SuspiciousFileOperation as e:
            logger.warning(
                "Skipping SuspiciousFileOperation during hashed_name lookup for file '%s'. "
                "The path resolves outside STATIC_ROOT. Returning original name.",
                name
            )
            # در صورت بروز خطا، نام اصلی فایل را برمی‌گردانیم تا Collectstatic ادامه یابد
            return name

    def post_process(self, *args, **kwargs):
        # این قسمت را از Whitenoise import می‌کنیم
        from whitenoise.storage import MissingFileError 
        
        # تکرار بر روی ژنراتور والد
        files_to_process = super().post_process(*args, **kwargs)
        
        for original_path, processed_path, processed in files_to_process:
            if isinstance(processed, Exception):
                # اگر خطا از نوع MissingFileError WhiteNoise یا SuspiciousFileOperation جنگو باشد
                if isinstance(processed, MissingFileError) or isinstance(processed, SuspiciousFileOperation):
                    logger.warning(
                        "Skipping StaticFiles Post-Processing Error (%s) for file '%s'. "
                        "This is often safe to ignore for third-party libraries.",
                        type(processed).__name__,
                        original_path
                    )
                    # ادامه فرآیند با فرض موفقیت
                    yield original_path, None, True
                else:
                    # ارسال مجدد سایر خطاها
                    yield original_path, processed_path, processed
            else:
                # ارسال نتایج موفق
                yield original_path, processed_path, processed


BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ۱. تنظیمات امنیتی و محیط Production
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-2=#49=b%(inur)!ev+ys^f6v$m=le9by)e4_du148e_gy28av')
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
    'django.contrib.messages', # <-- این اپ فعال است
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
    'django.contrib.messages.middleware.MessageMiddleware', # <-- این فعال است
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

# ==========================================================
# ۳. TEMPLATES (رفع خطای Admin.E404)
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
                'django.contrib.messages.context_processors.messages', # **<-- این خط خطا را برطرف می‌کند**
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

# نادیده گرفتن فایل‌های مشکل‌ساز در Collectstatic
STATICFILES_IGNORE_PATTERNS = [
    '*.map', 
    'assets/libs/@mdi/font/css/materialdesignicons.min.css',
]

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = BASE_DIR / "mediafiles"

# پیکربندی مدرن ذخیره‌سازی فایل‌ها (Django 4.0+)
STORAGES = {
    # استفاده از کلاس سفارشی برای نادیده گرفتن خطاهای WhiteNoise MissingFileError و SuspiciousFileOperation
    "staticfiles": {
        "BACKEND": "djangoProject.settings.CustomWhiteNoiseStaticFilesStorage",
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
# ۸. تنظیمات WhiteNoise (سختگیری کمتر)
# ==========================================================
WHITENOISE_IGNORE_FILE_TYPES = ['map', 'eot', 'ttf', 'woff', 'woff2', 'otf']
WHITENOISE_MANIFEST_STRICT = False


# ==========================================================
# ۹. تنظیمات LOGGING (برای رفع هشدارهای WhiteNoise)
# ==========================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        # سطح هشدار برای لاگر سفارشی WhiteNoise (مربوط به SuspiciousFileOperation)
        '__main__': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}


# ==========================================================
# ۱۰. متغیرهای سفارشی 
# ==========================================================
RESUME_NAME = os.environ.get('RESUME_NAME', 'رزومه خورشید ریانه (نسخه لوکال)')