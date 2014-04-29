"""
Django settings for PeeTwitt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCT = not 'MyProject' in BASE_DIR and not 'Chow' in BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x6n2qrky3^nlcl4w-t+v49af2ic3m=xt@8fr77fj2%*-1(3@)_'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

if not PRODUCT:
    DEBUG = True
    TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pee_user',
    'tweet',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'PeeTwitt.urls'

WSGI_APPLICATION = 'PeeTwitt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}
if not PRODUCT:
    from deploy.get_secret import get_password
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'PeeTwitt',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': get_password(),                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()


# Template setting
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(BASE_DIR, "templates")),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LOGIN_URL = 'pee_user_signup'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'purduetweet@gmail.com'
EMAIL_HOST_PASSWORD = 'putt@gmail'
EMAIL_PORT = 587