import os
import environ
from corsheaders.defaults import default_headers
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()
env.read_env(".env")


SECRET_KEY = env.str("SECRET_KEY", default='django-insecure-36_4n+f^f$#goaw7j1la^13i32n&7l+=1gc3ak851%tqv1@jzd')


ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])



# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


THIRD_PARTY_APPS = [
    'rest_framework',
    "rest_framework.authtoken",
    "corsheaders",
    "django_extensions",
    "django_filters",
    'coreapi',
    'drf_yasg',
]

LOCAL_APPS = [
    "spacecraft.apps.Config",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'demo.wsgi.application'

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
#MIGRATION_MODULES = {"sites": "contrib.sites.migrations"}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if env.str("ENVIRONMENT", default="production") == "local":
    DATABASES = {
            "default": env.db("DATABASE_URL", default="postgres:///db")
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("DJANGO_DATABASE_NAME"),
            "USER": env.str("DJANGO_DATABASE_USER"),
            "PASSWORD": env.str("DJANGO_DATABASE_PASSWORD"),
            "HOST": env.str("DJANGO_DATABASE_HOST"),
            "PORT": env.str("DJANGO_DATABASE_PORT", default=5432),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = str(BASE_DIR.path("staticfiles"))
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(BASE_DIR.path("static")),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# CORS SETTINGS
CORS_ALLOW_HEADERS = list(default_headers) + [
    "header", # custom header
    "baggage", # for sentry configuration
    "sentry-trace", # for sentry configuration
]

CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=True)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework Settings =============
PAGE_SIZE = env("PAGE_SIZE", default=50)
REST_FRAMEWORK = {
    # if not specified otherwise, anyone can access a view (this is the default)
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
        #"rest_framework.permissions.IsAuthenticated",
    ),
    # if required, which authentication is eligible?
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #"rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    # input formats the API can handle
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    #  output format supported by the API
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
        #"rest_framework.renderers.BrowsableAPIRenderer",
    ),
    # throttling of requests
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "2/second"},
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": PAGE_SIZE,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}