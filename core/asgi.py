"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from decouple import config as ENV
from django.core.asgi import get_asgi_application

DJANGO_SETTINGS_MODULE = ENV("DJANGO_SETTINGS_MODULE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

application = get_asgi_application()
