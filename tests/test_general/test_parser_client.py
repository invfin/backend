import pytest

from apps.general.outils.parser_client import ParserClient


@pytest.mark.django_db
class TestParserClient:
    @classmethod
    def setup_class(cls) -> None:
        cls.parser_client = ParserClient()
        cls.parser_client.base_path = "https://www.google.com/"
        cls.parser_client.api_version = None
        cls.parser_client.auth = None
        cls.path = "search"
        cls.dict_params = {
            "q": "galletas",
            "oq": "galletas",
            "aqs": "chrome..69i57.1073j0j1",
            "sourceid": "chrome",
            "ie": "UTF-8",
        }

    def test__build_full_path(self):
        multiple_params_url = (
            "https://www.google.com/search?q=galletas&oq=galletas&aqs=chrome..69i57.1073j0j1&sourceid=chrome&ie=UTF-8"
        )
        assert f"https://www.google.com/{self.path}" == self.parser_client._build_full_path(self.path)
        assert f"https://www.google.com/V6/{self.path}" == self.parser_client._build_full_path(
            self.path,
            "V6",
        )
        assert f"https://www.google.com/V6/{self.path}/str-params" == self.parser_client._build_full_path(
            self.path, "V6", "str-params"
        )
        assert multiple_params_url == self.parser_client._build_full_path(self.path, None, None, **self.dict_params)
        multiple_params_url_with_auth = (
            "https://www.google.com/search?token=password&q=galletas&oq=galletas"
            "&aqs=chrome..69i57.1073j0j1&sourceid=chrome&ie=UTF-8"
        )
        self.parser_client.auth = {"token": "password"}
        assert multiple_params_url_with_auth == self.parser_client._build_full_path(
            self.path, None, None, **self.dict_params
        )
