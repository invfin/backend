import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.urls import (
)

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

