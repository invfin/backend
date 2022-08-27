from django.apps import apps
from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.admin)
def jazzmin_menu_check(app_configs, **kwargs):
    """
    Checks all apps in django jazzmin custom menu exist.
    """

    errors = []

    for menu_name in ['side_menu_models']:
        menu = settings.JAZZMIN_SETTINGS.get(menu_name)
        for menu_elem in menu:
            for model in menu_elem.get('models', []):
                if isinstance(model, dict):
                    model = model.get('model')

                app_label, model_name = model.split('.')

                try:
                    apps.get_model(app_label, model_name)
                except LookupError:
                    errors.append(
                        Error(
                            f"Model `{model}` under label {menu_elem.get('label')} in "
                            f"JAZZMIN_SETTINGS.{menu_name} does not exist.",
                        )
                    )

    return errors
