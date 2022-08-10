import vcr
from model_bakery import baker

from django.test import TestCase

from {{app_name}}.{{file_name}} import (
{% for import in imports %}{{import}},
{% endfor %})

{{base_app_name}}_vcr = vcr.VCR(
    cassette_library_dir='cassettes/{{base_app_name}}/{{file_name}}/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

{% for clase in clases %}
class {{clase.class_naming}}(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    {% for function in clase.functions %}
    def {{function.function_namig}}(self):
        pass
    {% endfor %}
{% endfor %}