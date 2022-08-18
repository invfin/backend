import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.urls import (
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

