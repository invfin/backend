from .base import IS_PROD, env

from .ckeditor import *
from .custom_admin import *

if IS_PROD:
    from .production import *

    # REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]
else:
    if env.str("IS_TESTING", False):
        from .test import *
    else:
        from .local import *

        # REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.BrowsableAPIRenderer"]
