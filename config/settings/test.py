"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

from .ckeditor import *
from .custom_admin import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="jBxqwRsGQcTz3dV1o8quZxpFMyKBGhF2Olha3VTA7TTALWfgFkrLuY0dQYLoOnp7",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"
# TEST_RUNNER = "apps.general.tests.runner.PytestTestRunner"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("LOCAL_DATABASE_URL", default="postgresql://root@localhost/circle_test?sslmode=disable")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------
