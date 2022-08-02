from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MockRequest:
    pass


class {{base_app_name}}Admin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser()

        cls.model_admin = {{base_app_name}}Admin(model={{base_app_name}}, admin_site=AdminSite())

    def test_admin_changelist_pages(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("admin:{{app_name}}_{{model_name}}_changelist"),
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_change_page(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:{{app_name}}_{{model_name}}_change", args=[self.{{model_name}}.pk]))
        self.assertEqual(response.status_code, 200)

    def test_admin_delete_page(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:{{app_name}}_{{model_name}}_delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_admin_add_page(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "admin:{{app_name}}_{{model_name}}_add",
            )
        )
        self.assertEqual(response.status_code, 200)
