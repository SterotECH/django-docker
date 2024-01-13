import os
from datetime import timedelta
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key
import environ
environ.Env.read_env()

######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', get_random_secret_key())

DEBUG = os.environ.get('DEBUG', False)

LOCAL = os.environ.get('LOCAL', False)

ROOT_URLCONF = "backend.urls"

WSGI_APPLICATION = "backend.wsgi.application"

ASGI_APPLICATION = 'backend.asgi.application'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


######################################################################
# Domains
######################################################################

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:8000",
    "http://localhost:3001",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8000",
    "http://localhost:3001",
]

CORS_ALLOW_CREDENTIALS = True

######################################################################
# Apps
######################################################################

INSTALLED_APPS = [
        "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.simple_history",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_filters',
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt.token_blacklist",
    "import_export",
    'core.apps.CoreConfig',
]

######################################################################
# Middleware
######################################################################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

######################################################################
# Templates
######################################################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


######################################################################
# Databases
######################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    },
}

######################################################################
# Authentication
######################################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = 'core.User'

LOGIN_URL = "admin:login"

LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

######################################################################
# Localization
######################################################################

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Africa/Accra'

USE_I18N = True

USE_TZ = True

######################################################################
# Static
######################################################################

STATIC_URL = "static/"
STATICFILES_BASE_DIRS = BASE_DIR / "static"
STATICFILES_DIRS = [STATICFILES_BASE_DIRS]
if LOCAL:
    STATIC_ROOT = BASE_DIR / "local-cdn" / "static"
else:
    STATIC_ROOT = "/vol/web/static"

MEDIA_URL = "media/"

MEDIA_DIR = [BASE_DIR / "media"]

if LOCAL:
    MEDIA_ROOT = BASE_DIR / "local-cdn" / "media"
else:
    MEDIA_ROOT = "/vol/web/media"


######################################################################
# Cache
######################################################################
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
LOGGING_FILEHANDLER = 'logging.FileHandler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {module}: {name} - {message}',
            'style': '{'
        },
        'simple': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'class': LOGGING_FILEHANDLER,
            'filename': os.path.join(BASE_DIR, 'log/general.log'),
            'formatter': 'verbose'
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': LOGGING_FILEHANDLER,
            'filename': os.path.join(BASE_DIR, 'log/debug.log'),
            'formatter': 'verbose',
        },
        'error_log_file': {
            'level': 'ERROR',
            'class': LOGGING_FILEHANDLER,
            'filename': os.path.join(BASE_DIR, 'log/error.log'),
            'formatter': 'verbose',
        },
        'info_log_file': {
            'level': 'INFO',
            'class': LOGGING_FILEHANDLER,
            'filename': os.path.join(BASE_DIR, 'log/info.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['debug_log_file', 'file', 'info_log_file', 'error_log_file', 'console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django': {
            'handlers': ['error_log_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

######################################################################
# Rest Framework
######################################################################
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "10000/day"},
    "DEFAULT_PAGINATION_CLASS": "core.pagination.StandardResultSetPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "SEARCH_PARAM": 'q'
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": "JWT",
}

ADMINS = [("stero", "agyeistero@gmail.com")]

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

SPECTACULAR_SETTINGS = {
    "TITLE": "Edu Manage Pro",
    "DESCRIPTION": "Django Docker Startup Template",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": "Stero Docker Admin",
    "SITE_TITLE": "Stero Docker Admin",
    "ENVIRONMENT": "backend.utils.environment_callback",
    "DASHBOARD_CALLBACK": "backend.utils.dashboard_callback",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SCRIPTS": [
        lambda request: static("js/chart.min.js"),
    ],
    "LOGIN": {
        "image": lambda r: static("images/login-bg.jpg"),
        "redirect_after": None,
    },
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
        },

    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _(""),
                "separator": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:core_user_changelist"),
                        "badge": "backend.utils.badge_callback",
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ]
            },
        ],
    },
}
