import os
from django.urls import reverse_lazy
from pathlib import Path
from dotenv import load_dotenv
from utils.converters import to_int_or_default


# Loads environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "false") == "true"

AZURE_WEBSITE_HOSTNAME = os.getenv("WEBSITE_HOSTNAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + ([AZURE_WEBSITE_HOSTNAME] if AZURE_WEBSITE_HOSTNAME is not None else [])
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'django.contrib.flatpages',
    "django_bootstrap5",
    "widget_tweaks",
    "ckeditor",
    "treebeard",
    "phonenumber_field",
    "base",
    "contacts",
    "regulations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "base.context_processors.metadata",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DBNAME", default="postgres"),
        "USER": os.getenv("DBUSER", default="postgres"),
        "PASSWORD": os.getenv("DBPASS", default="postgres"),
        "HOST": os.getenv("DBHOST", default="localhost"),
        "PORT": to_int_or_default(os.getenv("DBPORT"), default=5432),
    }
}

DB_SEARCH_CONFIG = "english_nostop"


# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


def gettext_noop(s):
    return s


LANGUAGES = (
    ("en", gettext_noop("English")),
    ("no", gettext_noop("Norwegian")),
)


# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public/static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# public files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'config/public/media')

# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# HOMEPAGE
HOMEPAGE = reverse_lazy("front_page")

# DEFAULTS
SITE_ID = 1
SITE_NAME = "Export Control"
SITE_TAGLINE = "Safetec"
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

LOCALE_PATHS = [BASE_DIR /'locale']
JAZZMIN_SETTINGS = {
    "site_title": "ExportControl Admin",
    "site_header": "ExportControl Admin",
    "site_logo": "base/img/logo/safetec-logosymbol-rgb-10px.png",
    "site_brand": "Export Control",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Admin Panel Control",
    "copyright": "ExportControl Admin Panel Control",
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site", "url": "front_page", "new_window": True},
        {"name": "Search", "url": "search", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": False,
}

