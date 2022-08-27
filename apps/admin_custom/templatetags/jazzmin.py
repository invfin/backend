from collections import defaultdict
# import copy
# import json
from typing import List

from django.contrib.admin.helpers import AdminForm, InlineAdminFormSet
# from django.contrib.admin.models import LogEntry
# from django.template import Context
# from django.urls import reverse
from django.utils.text import capfirst
# from django.utils.translation import gettext

# from jazzmin.settings import get_settings
from jazzmin.templatetags.jazzmin import (
    # action_message_to_list as jazzmin_action_message_to_list,
    register,
)



# @register.simple_tag(name='get_side_menu', takes_context=True)
# def get_side_menu(context: Context, using: str = "available_apps") -> List[Dict]:
#     """
#     Overrides Django Jazzmin get_side_menu templatetag.

#     Permissions are not checked here, as context["available_apps"] has already been filtered by
#     django
#     """

#     menu = []
#     options = get_settings()
#     menu_config = get_menu_config(context, options)
#     available_apps = copy.deepcopy(context.get(using, []))

#     for elem in menu_config:
#         sub_menu = []

#         # Models
#         for model in elem.get('models', []):
#             if isinstance(model, dict):
#                 model_id = model.get('model')
#                 model_label = model.get('label')
#             else:
#                 model_id = model
#                 model_label = None

#             model_name, model_url = get_model_data(model_id, available_apps)
#             if model_name and model_url:
#                 sub_menu.append({
#                     'name': model_label or model_name,
#                     'url': model_url,
#                     'icon': options["default_icon_children"],
#                 })

#         # Custom links
#         for link in elem.get('custom_links', []):
#             url = link.get('url')  # Direct URL

#             url_name = link.get('url_name')
#             if url_name:
#                 # URL by django view name
#                 url = reverse(url_name)

#             if url:
#                 sub_menu.append({
#                     'name': link.get('label'),
#                     'url': url,
#                     'icon': options["default_icon_children"],
#                 })

#         if sub_menu:
#             menu.append({
#                 'name': elem.get('label'),
#                 'icon': elem.get('icon', options["default_icon_parents"]),
#                 'models': sub_menu,
#             })

#     return menu


# def get_menu_config(context: Context, options) -> list:
#     if not context:
#         return []

#     user = context.get("user")

#     if not user or user.is_anonymous:
#         return []


#     return options.get('side_menu_models', [])


# def get_model_data(model_id, available_apps):
#     """
#     model_id is a string with this format <app_name>.<model_name>
#     available_apps is an array of available models for the current user.

#     Iterates over all available_apps and returns the model name and its admin url if the user has
#     view permissions.
#     """

#     app_label, model_label = model_id.split('.')

#     for app in available_apps:
#         if app.get('app_label') == app_label:
#             for model in app.get('models', []):
#                 model_url = model.get('admin_url')

#                 # Get model label from the admin url
#                 label = '.'.join(model_url.rstrip('/').lstrip('/').split('/'))

#                 if label == model_id:
#                     return model.get('name'), model_url

#     return None, None


class CustomTab:
    template = None
    custom_tab = True

    def __init__(self, template):
        self.template = template


@register.simple_tag(name='get_tabs')
def get_tabs(
    admin_form: AdminForm,
    inline_admin_formsets: List[InlineAdminFormSet],
) -> List:
    """
    Overrides Django Jazzmin get_sections templatetag in order to add tabs with custom content.

    tabs = [
        {
            'id': 'general',
            'name': "Trip details",
            'items' : [Formset, inline],
        },
        ...
    ]
    """

    tabs = []

    if hasattr(admin_form.model_admin, 'jazzmin_form_tabs'):
        items_dict = defaultdict(list)

        # Fieldsets
        for fieldset in admin_form:
            if fieldset.classes.startswith('jazzmin-tab'):
                jazzmin_tab_id = fieldset.classes.replace('jazzmin-tab-', '')
            else:
                jazzmin_tab_id = 'general'
            items_dict[jazzmin_tab_id].append(fieldset)

        # Inlines
        for inline in inline_admin_formsets:
            inline.is_inline = True
            jazzmin_tab_id = inline.opts.jazzmin_tab_id
            items_dict[jazzmin_tab_id].append(inline)

        # Custom Tabs
        if hasattr(admin_form.model_admin, 'jazzmin_custom_tabs'):
            for tab_id, template in admin_form.model_admin.jazzmin_custom_tabs:
                tab = CustomTab(template)
                items_dict[tab_id].append(tab)

        # Form includes
        if hasattr(admin_form.model_admin, 'jazzmin_form_includes'):
            for template, position, tab_id in admin_form.model_admin.jazzmin_form_includes:
                tab = CustomTab(template)
                if position == 'top':
                    items_dict[tab_id].insert(0, tab)
                else:
                    items_dict[tab_id].append(tab)

        jazzmin_form_tabs = admin_form.model_admin.jazzmin_form_tabs
        for tab_id, tab_name in jazzmin_form_tabs:
            tabs.append({
                'id': tab_id,
                'name': tab_name,
                'items': items_dict[tab_id],
            })
    else:
        fieldsets = [x for x in admin_form]

        # Make inlines behave like formsets
        for fieldset in inline_admin_formsets:
            fieldset.name = capfirst(fieldset.opts.verbose_name_plural)
            fieldset.is_inline = True
            fieldsets.append(fieldset)

        tabs.append({
            'id': 'general',
            'name': "General",
            'items': fieldsets,
        })

    return tabs


# @register.simple_tag
# def action_message_to_list(action: LogEntry) -> List[Dict]:
#     """
#     Django template tag that has been overrided by Jazzmin. It's used to show all logs related
#     to a given instance. The Jazzmin's change adds icons and colors to the object_history
#     We override it again to add a viewed function that enables to display "Viewed" in the
#     object_history of the sensitive area.
#     action.change_message is generated by Django and returns a string. Then it serializes
#     the messages and if there is "viewed", "read" or any (CRUD) verb it passes it through
#     is given function to return and display an icon and color according
#     """
#     if action.action_flag != LOG_ENTRY_FLAG_VIEW:
#         return jazzmin_action_message_to_list(action)

#     messages = []

#     def viewed(x: str) -> Dict:
#         return {
#             "msg": x,
#             "icon": "eye",
#             "colour": "warning",
#         }

#     if action.change_message and action.change_message[0] == "[":

#         try:
#             change_message = json.loads(action.change_message)
#         except json.JSONDecodeError:
#             return [action.change_message]

#         for sub_message in change_message:

#             if "viewed" in sub_message:
#                 messages.append(viewed(gettext("Viewed")))

#     return messages
