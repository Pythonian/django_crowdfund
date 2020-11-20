import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG"))

ALLOWED_HOSTS = ['127.0.0.1:8000', '127.0.0.1', 'www.whenwillibefamous.com', 'whenwillibefamous.com']


# Application definition

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
]

#PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL')
PAYPAL_RECEIVER_EMAIL = 'McCartneysystems@gmail.com'
#PAYPAL_TEST = os.getenv('PAYPAL_TEST')
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'static_root'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

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

# Goal amount (int) that you are trying to raise.
GOAL = 25000

PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')

AUTHOR_EMAIL = os.getenv('AUTHOR_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '93dad87dab41b7'
EMAIL_HOST_PASSWORD = '3d2294bed0d58f'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True

SECURE_HSTS_SECONDS = 2592000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True
