from .dev import *  # noqa
import os

DEBUG = False

# Get allowed hosts from environment variable, default to localhost
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
