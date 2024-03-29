import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!e8xkh)#2#eh*z69ji=y34i2r&wyr%bm3!8l+#z1ui+-!1yqja'

DEBUG = False

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = 10021440

INSTALLED_APPS = [
    'v2',
    'channels',
    'accounting',
    'payment',
    'sales',
    'inventory',
    'user_handler',
    'corsheaders',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simple_im.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build'), os.path.join(BASE_DIR, 'template')],
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

WSGI_APPLICATION = 'simple_im.wsgi.application'
ASGI_APPLICATION = "simple_im.routing.application"


DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'erp',
        'USER': 'main_user',
        'PASSWORD': 'p@ssw0rd',
        'HOST': 'localhost',
        'PORT': 5432,
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

LOGIN_REDIRECT_URL = ''
LOGIN_URL='/login'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")



AUTH_USER_MODEL = 'user_handler.CustomUserBase'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000' # Here was the problem indeed and it has to be http://localhost:3000, not http://localhost:3000/
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_COOKIE_NAME = 'x-csrftoken'

CSRF_TRUSTED_ORIGINS = [
    'localhost:3000','localhost:8000','*'
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "build", "static"),  # update the STATICFILES_DIRS
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=12),
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}


EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = '2525'

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
date = datetime.date.today()
time = str(datetime.datetime.now().time()).split('.')[0]
location = BASE_DIR+'/backups/'+str(date)+'/'+time
DBBACKUP_STORAGE_OPTIONS = {'location': location}
DBBACKUP_FILENAME_TEMPLATE = 'database__{datetime}.backup'
DBBACKUP_MEDIA_FILENAME_TEMPLATE = 'mediafiles__{datetime}.tar'

# import channels_redis
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [("localhost", 6379)],
#         },
#     },
# }

from redislite import Redis
rdb = Redis('/tmp/redis.db', serverconfig={'port': '6379'})

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

RUN_MIGRATION = True

import mimetypes
mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)

WHITENOISE_MIMETYPES = {
    '.js': 'application/javascript',
    '.css': 'text/css'
}
