from pathlib import Path
import os
from environs import Env
# import django_on_heroku
from datetime import timedelta
from decouple import config
from dj_database_url import parse as db_url

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'django-insecure-(_8n3s3!npb-7vl24xat0ugyb_)=qa(sj5gdcua0_g&-xuu0g*'
SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env('DEBUG')


ALLOWED_HOSTS = env('ALLOWED_HOSTS')
# ALLOWED_HOSTS = ['*']

# # AWS S3 SETTINGS
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_URL = os.environ.get('AWS_URL')
# AWS_DEFAULT_ACL = None
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_S3_SIGNATURE_VERSION = 's3v4'

if not DEBUG:
    # Cloudinary stuff
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': env('CLOUD_NAME'),
        'API_KEY': env('API_KEY'),
        'API_SECRET': env('API_SECRET'),
    }

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # libraries
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'multiselectfield',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'ckeditor',
    'ckeditor_uploader',
    'braces',
    # 'parler',
    'cloudinary',
    'cloudinary_storage',

    # apps
    'user',
    'article',
    'masterclass',
    'courses',
    'adventure',
    'webinar',
    'membership'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'margulan.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'margulan.wsgi.application'

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url
    )
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'webilim',
#         'USER': 'webilim123',
#         'PASSWORD': 'password',
#         'HOST': 'postgres_db',
#         'PORT': '',
#     }
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 5,

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
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

# STATIC_URL = AWS_URL + '/static/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = AWS_URL + '/media/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=200),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
        # 'extraPlugins': ','.join(
        #     [
        #        'html5audio',
        #     ]
        # ),
    },
}
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True


gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russian')),
    ('ky', gettext('Kyrgyz')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.CustomUser'

# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER=env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=env.str('EMAIL_HOST_PASSWORD')


CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


PAY_SECRET_KEY = 'akEVO9a8iqoxXkzk'
MERCHANT_ID = '542306'
BASE_URL = "https://api.paybox.money/"
# CALLBACK_BASE_URL = "https://127.0.0.1:8000/"
CALLBACK_BASE_URL = "https://webilim.kg/time-out/"

# django_on_heroku.settings(locals())


