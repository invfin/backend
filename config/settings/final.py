from .base import env

IS_PROD = env.bool("IS_PROD", False)

if IS_PROD:
    from .production import *
else:
    from .local import *
