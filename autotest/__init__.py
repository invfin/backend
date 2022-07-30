from django.conf import settings

import django

from django.conf import settings

default_app_config = 'my_package.apps.MyPackageConfig'

if not settings.configured:s
    # Get the list of attributes the module has
    attributes = dir(overridden_settings)
    conf = {}

    for attribute in attributes:
        # If the attribute is upper-cased i.e. a settings variable, then copy it into conf
        if attribute.isupper():
            conf[attribute] = getattr(overridden_settings, attribute)

    # Configure settings using the settings
    settings.configure(**conf)
    
    # This is needed since it is a standalone django package
    django.setup()