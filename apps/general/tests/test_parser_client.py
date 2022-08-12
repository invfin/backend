from django.test import TestCase

from apps.general.outils.parser_client import ParserClient


class TestParserClient(TestCase):
    def setUpTestData(cls) -> None:
        cls.parser_client = ParserClient()
        cls.base_path = "https://www.google.com/"
        cls.path = "search"
        cls.api_version = None
        cls.str_params = None
        cls.dict_params = {
            "q": "galletas",
            "oq": "galletas",
            "aqs": "chrome..69i57.1073j0j1",
            "sourceid": "chrome",
            "ie": "UTF-8",
        }

    def test__build_full_path(self):
        multiple_params_url = (
            'https://www.google.com/search?q=galletas&oq=galletas'
            '&aqs=chrome..69i57.1073j0j1&sourceid=chrome&ie=UTF-8'
        )
        self.assertEqual(
            f"{self.base_path}{self.path}",
            self.parser_client._build_full_path(self.base_path, self.path)
        )
        self.assertEqual(
            f"{self.base_path}{self.path}",
            self.parser_client._build_full_path(self.base_path, self.path,self. api_version, self.str_params)
        )
        self.assertEqual(
            multiple_params_url,
            self.parser_client._build_full_path(self.base_path, self.path, self.api_version, self.str_params, self.dict_params)
        )
