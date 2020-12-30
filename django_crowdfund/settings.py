import django_heroku
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG'))

ALLOWED_HOSTS = ['127.0.0.1', 'www.whenwillibefamous.com', 'whenwillibefamous.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crowdfund',

    'paystack.frameworks.django',
    'paypal.standard.ipn',
    'imagekit',
    'ckeditor',
    'ckeditor_uploader',
]

PAYPAL_RECEIVER_EMAIL = 'McCartneysystems@gmail.com'
PAYPAL_TEST = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_crowdfund.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'paystack': 'paystack.frameworks.django.templatetags.paystack',
            },
        },
    },
]

WSGI_APPLICATION = 'django_crowdfund.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'static_root'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# /media/blog/image.jpg
CKEDITOR_UPLOAD_PATH = 'blog/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# Braintree settings

# BRAINTREE_MERCHANT_ID = os.getenv('BRAINTREE_MERCHANT_ID')
# BRAINTREE_PUBLIC_KEY = os.getenv('BRAINTREE_PUBLIC_KEY')
# BRAINTREE_PRIVATE_KEY = os.getenv('BRAINTREE_PRIVATE_KEY')

# import braintree

# BRAINTREE_CONF = braintree.Configuration(
#     braintree.Environment.Sandbox,
#     BRAINTREE_MERCHANT_ID,
#     BRAINTREE_PUBLIC_KEY,
#     BRAINTREE_PRIVATE_KEY
# )

# Amount that you are trying to raise.
GOAL = '25000'

PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

AUTHOR_EMAIL = os.getenv('AUTHOR_EMAIL')
DEFAULT_FROM_EMAIL = os.getenv('AUTHOR_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = True

if not DEBUG:
    SECURE_HSTS_SECONDS = 2592000
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_PRELOAD = True

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

django_heroku.settings(locals())