from .base import env

IS_PROD = env.bool("IS_PROD", False)

from .ckeditor import *
from .custom_admin import *

if IS_PROD:
    from .production import *
    PROTOCOL = "https://"
else:
    PROTOCOL = "http://"
    from .local import *
