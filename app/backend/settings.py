import os
from datetime import timedelta
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import environ
# reading .env file
environ.Env.read_env()

######################################################################
# General
######################################################################

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-yven9*vd5-h=7a9pe=k0c1h9mr%-7-=us)2ygbh^_-pf+%lna9"

DEBUG = True

ROOT_URLCONF = "backend.urls"

WSGI_APPLICATION = "backend.wsgi.application"

ASGI_APPLICATION = 'backend.asgi.application'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


######################################################################
# Domains
######################################################################

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://0.0.0.0:8000',
    'http://localhost:3001',
]

CORS_ALLOW_CREDENTIALS = True

######################################################################
# Apps
######################################################################

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    "django_celery_beat",
    'core.apps.CoreConfig',
]

######################################################################
# Middleware
######################################################################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.middleware.ReadonlyExceptionHandlerMiddleware",
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

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

######################################################################
# Static
######################################################################

STATIC_URL = "static/"
STATICFILES_BASE_DIRS = BASE_DIR / "static"
STATICFILES_DIRS = [STATICFILES_BASE_DIRS]
STATIC_ROOT = "/vol/web/static"

MEDIA_URL = "media/"

MEDIA_DIR = [
    BASE_DIR / 'media'
]

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

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

######################################################################
# Rest Framework
######################################################################
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
}

ADMINS = [
    ('stero', 'agyeistero@gmail.com')
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '<email>'
EMAIL_HOST_PASSWORD = '<password>'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": "DJango Admin",
    "SITE_TITLE": "DJango Admin",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SCRIPTS": [
        lambda request: static("js/chart.min.js"),
    ],
    "STYLES": [
        lambda request: static("css/styles.css"),
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
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _(""),
                "separator": False,  # Top border
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
