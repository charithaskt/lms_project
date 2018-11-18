import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u90cspyw*so$&3k29#7=(w*us$xuwgiith47q-esbsr=1iu=jz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

JWTAUTH=False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken', 
    'explorer',
    'django_tables2',
    'django_filters',
    'bootstrap3',
    'intranet',
    'accounts',
    'opac',
    'ilsapi',
    'photos',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # new cors for react
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:3000/' #react app frontend url
)

ROOT_URLCONF = 'custom_user_model.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
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

WSGI_APPLICATION = 'custom_user_model.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
AUTH_USER_MODEL='accounts.User'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

if JWTAUTH:
    REST_FRAMEWORK = {
        # When you enable API versioning, the request.version attribute will contain a string
        # that corresponds to the version requested in the incoming client request.
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
        # Permission settings
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ],
        # Authentication settings
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ]

    } 

else:
    REST_FRAMEWORK = {
        # When you enable API versioning, the request.version attribute will contain a string
        # that corresponds to the version requested in the incoming client request.
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
        # Permission settings
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ],
        # Authentication settings
        'DEFAULT_AUTHENTICATION_CLASSES': [
            #'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.TokenAuthentication', 
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4

    }
#JWT settings
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=600),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}

EXPLORER_CONNECTIONS = { 'Default': 'default' }
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_PERMISSION_VIEW = lambda u: u.is_staff
EXPLORER_PERMISSION_CHANGE = lambda u: u.is_admin

EXPLORER_TRANSFORMS = [
  ('author', '<a href="http://localhost:8000/catalog/author/{0}/">{0}</a>'),
  ('biblio', '<a href="http://localhost:8000/catalog/book/{0}/">{0}</a>'),
  ('item', '<a href="http://localhost:8000/catalog/item/{0}/">{0}</a>'),
  ('publisher', '<a href="http://localhost:8000/catalog/publisher/{0}/">{0}</a>'),
  ('genre', '<a href="http://localhost:8000/catalog/genre/{0}/">{0}</a>'),
  ('suggestion', '<a href="http://localhost:8000/api/v1/suggestion/{0}/">{0}</a>'),
]
EXPLORER_UNSAFE_RENDERING=True
EXPLORER_CSV_DELIMETER=','
EXPLORER_TOKEN_AUTH_ENABLED=True
EXPLORER_TOKEN='@#kjlk^&(&099-jioiououu668686vf76r7f76447urt'
EXPLORER_SQL_WHITELIST=('CREATED', 'UPDATED', 'DELETED','REGEXP_REPLACE','REPLACE')
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'custom_user_model/static'),
)
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
#LOGIN_URL = 'ils-login'
#LOGOUT_URL = 'ils-logout'

LOGIN_REDIRECT_URL = 'profile_detail'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'example.com'
#EMAIL_HOST_PASSWORD = 'secret'
#EMAIL_PORT = 587

