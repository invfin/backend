from unittest import TestCase

from apps.api.mixins import APIViewTestMixin


class TestAPIViewTestMixin(TestCase):
    def test_no_attribute_defined(self):
        class Foo(APIViewTestMixin):
            pass

        with self.assertRaises(AttributeError):
            Foo().test_verbs()

    def test_attribute_not_a_set(self):
        class Foo(APIViewTestMixin):
            allowed_verbs = []  # should be a set

        with self.assertRaises(TypeError):
            Foo().test_verbs()
