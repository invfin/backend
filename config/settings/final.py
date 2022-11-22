from .base import IS_PROD, IS_TEST

from .ckeditor import *
from .custom_admin import *

if IS_PROD:
    from .production import *
elif IS_TEST:
    from .test import *
else:
    from .local import *
