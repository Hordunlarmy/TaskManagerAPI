import os  # noqa
from datetime import timedelta

from decouple import config as ENV
from django.contrib import admin

from .base import *  # noqa

SECRET_KEY = ENV("SECRET_KEY")


THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_standardized_errors",
    "corsheaders",
    "debug_toolbar",
]


LOCAL_APPS = [
    "src.oauth",
    "src.user",
    "src.task",
]


INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS  # noqa

MIDDLEWARE += [  # noqa
    "corsheaders.middleware.CorsMiddleware",  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "EXCEPTION_HANDLER": "core.exception_handler.custom_exception_handler",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
    ],
}

SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"Basic": {"type": "basic"}}}


# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
#
# SIMPLE_JWT_SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": "HS384",
    "SIGNING_KEY": SECRET_KEY,
}

CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0",
]


APPEND_SLASH = True
AUTH_USER_MODEL = "user.User"


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    if not app_dict:
        return
    return list(app_dict.values())


admin.AdminSite.get_app_list = get_app_list
