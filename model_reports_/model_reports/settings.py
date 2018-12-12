import os
import datetime
#djk
import random
import hashlib
from django.utils import timezone
from django.utils.version import get_version
from distutils.version import LooseVersion
#djk
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u90cspyw*so$&3k29#7=(w*us$xuwgiith47q-esbsr=1iu=jz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#paytm
PAYTM_MERCHANT_KEY = ""
PAYTM_MERCHANT_ID = ""
HOST_URL = "http://localhost:8000/"
PAYTM_CALLBACK_URL = "payment/check/"

if DEBUG:
    PAYTM_MERCHANT_KEY = "T1GsewDpWX%z3BdZ"
    PAYTM_MERCHANT_ID = "xNaORM51969003078152"
    PAYTM_WEBSITE = 'WEBSTAGING'
    HOST_URL = "http://localhost:8000"
    '''
    In sandbox enviornment you can use following wallet credentials to login and make payment.
    Mobile Number : 7777777777
    Password : Paytm12345
    This test wallet is topped-up to a balance of 7000 Rs. every 5 minutes.
    While paying... Select the option "pay with paytm wallet". Then the mobile number is 7777777777 and the otp is 489871
    '''
#paytm
#dkj
JS_ERRORS_ALERT = DEBUG
# Requires proper setup of Django email error logging.
JS_ERRORS_LOGGING = not DEBUG
#dkj
JWTAUTH=False
DJK=True
LDAP=False

ALLOWED_HOSTS = []
#dkj
DJK_APPS = (
    'djk_sample',
    'ils_app',
    'event_app',
)
#dkj

# Application definition

INSTALLED_APPS = (
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
    'idapp',
    'payment',
    'photos',
    'rssfeed',
    'djangoql',
    'reg.apps.RegConfig', #sreeja
    #dkj
    # 'sites' is required by allauth
    'django.contrib.sites',
    'django_jinja',
    'django_jinja.contrib._humanize',
    'django_jinja_knockout',
    'django_jinja_knockout._allauth',
    #dkj
) + DJK_APPS + (
    'allauth',
    'allauth.account',
    # Required for socialaccount template tag library despite we do not use social login
    'allauth.socialaccount',
)
#djk
# For simple cases it is enough to include original middleware (commented out).
DJK_MIDDLEWARE = 'djk_sample.middleware.ContextMiddleware'
# DJK_MIDDLEWARE = 'django_jinja_knockout.middleware.ContextMiddleware'
#djk

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#react
CORS_ORIGIN_WHITELIST = (
    'localhost:3000/' #react app frontend url
)
#djk
if LooseVersion(get_version()) >= LooseVersion('1.11'):
    MIDDLEWARE.append(DJK_MIDDLEWARE)
else:
    MIDDLEWARE_CLASSES = MIDDLEWARE
    MIDDLEWARE.extend([
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        DJK_MIDDLEWARE,
    ])
#djk

ROOT_URLCONF = 'model_reports.urls'

#djk
#if DJK==True:
try:
    # Django > 1.9
    from django.template.context_processors import i18n
    i18n_processor = 'django.template.context_processors.i18n'
except ImportError:
    from django.core.context_processors import i18n
    i18n_processor = 'django.core.context_processors.i18n'

#djk

TEMPLATES = [
    #djk
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".htm",
            "app_dirname": "jinja2",
            'context_processors': [
                i18n_processor,
                # For simple cases it is enough to include original template context processor (commented out).
                'djk_sample.context_processors.template_context_processor'
                # 'django_jinja_knockout.context_processors.template_context_processor'
            ]
        },
    },
    #djk
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),os.path.join(BASE_DIR,'templates/ASE'),os.path.join(BASE_DIR,'custom_user_model/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Next line is required only if project uses Django templates (DTL).
                'djk_sample.context_processors.template_context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'model_reports.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #djk
        'TEST': {
            'NAME': ':memory:',
        },
    },
    #'production': {
        #'ENGINE': 'django.db.backends.mysql',
        #'OPTIONS': {
            #'read_default_file': '/etc/mysql/my.cnf',
        #},
    #},
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
  ('author', '<a href="http://localhost:8000/catalog/author/{0}/">{0}</a>'),#
  ('biblio', '<a href="http://localhost:8000/catalog/book/{0}/">{0}</a>'),#
  ('item', '<a href="http://localhost:8000/catalog/item/{0}/">{0}</a>'),
  ('publisher', '<a href="http://localhost:8000/api/v1/publisher/{0}/">{0}</a>'),#
  ('genre', '<a href="http://localhost:8000/api/v1/genre/{0}/">{0}</a>'),#
  ('suggestion', '<a href="http://localhost:8000/api/v1/suggestion/{0}/">{0}</a>'),#
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
#djk
# Use django_jinja_knockout app.js / middleware.py to detect timezone from browser.
USE_JS_TIMEZONE = True
#djk

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#djk
VUE_INTERPOLATION = False
#djk
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'model_reports/static'),
)
#djk
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Next setting is required so multiple Django instances running at the same host/IP with different ports
# do not interfere each other (apollo13).
hash_obj = hashlib.md5(BASE_DIR.encode('utf-8'))
SESSION_COOKIE_NAME = 'djk_sessionid_{}'.format(hash_obj.hexdigest())
# For 'allauth'.
SITE_ID = 1
# Prevents infinite redirect when user has no permission to access current view.
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ALLAUTH_DJK_URLS = True
#djk
if DJK==True:
  # Login / logout for allauth.
  #LOGIN_URL = '/accounts/login/'
  #LOGIN_REDIRECT_URL = "/"
  #LOGOUT_URL = '/accounts/logout/'

  # Pagination settings.
  OBJECTS_PER_PAGE = 3 if DEBUG else 10

  # unit testing settings
  FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
  )
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
#LOGIN_URL = 'ils-login'
#LOGOUT_URL = 'ils-logout'
LOGIN_REDIRECT_URL = 'profile_detail'
#sreeja
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'aselib123@gmail.com'
EMAIL_HOST_USER = 'aselib123@gmail.com'
EMAIL_HOST_PASSWORD = 'library@18'
SERVER_EMAIL = 'aselib123@gmail.com'
#sreeja
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, GroupOfUniqueNamesType

# Baseline configuration.
AUTH_LDAP_SERVER_URI = 'ldap://localhost'

AUTH_LDAP_BIND_DN = 'cn=admin,dc=iiitslibrary,dc=org'
AUTH_LDAP_BIND_PASSWORD = '@dmin123'
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'ou=users,dc=iiitslibrary,dc=org',
    ldap.SCOPE_SUBTREE, 
    '(mail=%(user)s)',
)
AUTH_LDAP_USER_ATTR_MAP = {
    'fullname': 'givenName',
    'email': 'mail',
}


# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
#AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguised names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.

if LDAP==True:
   AUTHENTICATION_BACKENDS = (
      'django_auth_ldap.backend.LDAPBackend',
      'django.contrib.auth.backends.ModelBackend',
   )

if DJK==True:
   AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    #`allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
if LDAP==True:
  LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
  }
elif DJK==True:
  LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_log.sql'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
  }
