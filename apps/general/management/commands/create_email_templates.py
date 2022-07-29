from os.path import exists

from django.conf import settings
from django.core.management import BaseCommand
from django.db import connection

from apps.web.constants import CONTENT_PURPOSES


TEMPLATE_CONTENT =("""
{% extends "emailing/base.html" %}
{% block content %}
<p>{{first_intro}}{{user.full_name}}{{second_intro}}
    <br>
    {{content|safe}}        
</p>
<br>
{{first_goodbye}}
<br>
Lucas Montes - Inversiones & Finanzas
{% endblock content %}
""")


class Command(BaseCommand):

    def handle(self, *args, **options):
        for content in CONTENT_PURPOSES:
            template = f"{settings.APPS_DIR}/general/templates/emailing/web/{content[0]}.html"
            if not exists(template):
                with open(template, 'w') as f:
                    f.write(TEMPLATE_CONTENT)