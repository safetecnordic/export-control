import os
from django.urls import reverse_lazy
from pathlib import Path
from dotenv import load_dotenv
from exportcontrol.utils import to_int_or_default


# Path helper
def location(x):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)


# Loads environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "false") == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "widget_tweaks",
    "ckeditor",
    "treebeard",
    "phonenumber_field",
    "regulations",
    "base",
    "contacts",
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
]

ROOT_URLCONF = "exportcontrol.urls"

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

WSGI_APPLICATION = "exportcontrol.wsgi.application"


# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", default="postgres"),
        "USER": os.getenv("DB_USER", default="postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", default="postgres"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": to_int_or_default(os.getenv("DB_PORT"), default=5432),
    }
}

# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
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
STATIC_ROOT = location("public/static")
STATICFILES_DIRS = (location("static/"),)

# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# HOMEPAGE
HOMEPAGE = reverse_lazy("presentation")

# DEFAULTS
SITE_NAME = "ExportControl"
SITE_TAGLINE = "Legislation"
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
