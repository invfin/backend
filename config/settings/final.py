from .base import IS_PROD

from .ckeditor import *
from .custom_admin import *

if IS_PROD:
    from .production import *

    # REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]
else:
    from .local import *

    # REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.BrowsableAPIRenderer"]
