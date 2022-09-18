from .base import IS_PROD

from .ckeditor import *
from .custom_admin import *

if IS_PROD:
    from .production import *
else:
    from .local import *
