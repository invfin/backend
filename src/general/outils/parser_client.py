from typing import Union, Dict, Any
import requests
import time
import urllib

from src.general.constants import HEADERS, REQUESTS_MAX_RETRIES


class ParserClient:
    base_path: str = None
    api_version: str = None
    auth: Dict[str, str] = None

    def _build_full_path(
        self, path: str, different_api_version: str = None, str_params: str = None, **dict_params: dict
    ) -> str:
        """
        It receives the path from path to make the get requests. It accepts url depending on
        the information required and extra_params that can vary from one url to another.
        """
        full_path = self.base_path
        dict_params_separator = "?"
        if different_api_version:
            full_path = f"{full_path}{different_api_version}/"
        if not different_api_version and self.api_version:
            full_path = f"{full_path}{self.api_version}/"
        full_path = f"{full_path}{path}"
        if str_params:
            full_path = f"{full_path}/{str_params}"
        if self.auth:
            auth_dict = urllib.parse.urlencode(self.auth)
            full_path = f"{full_path}?{auth_dict}"
            dict_params_separator = "&"
        if dict_params:
            if "dict_params" in dict_params:
                dict_params = dict_params["dict_params"]
            dict_params = urllib.parse.urlencode(dict_params)
            full_path = f"{full_path}{dict_params_separator}{dict_params}"
        return full_path

    def _request_content(self, full_url: str) -> Union[Dict[str, Any], str, str, requests.Response]:
        """
        It performs a get request. full_url comes from _build_full_path.
        """
        for attempt in range(1, REQUESTS_MAX_RETRIES):
            response = requests.get(full_url, headers=HEADERS)
            if response.status_code == requests.codes.ok:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return response.json()
                if "text/csv" in content_type:
                    return response.text
                if "text/plain" in content_type:
                    return response.text
                else:
                    return response
            time.sleep(attempt * REQUESTS_MAX_RETRIES)
        response.raise_for_status()

    def request(self, path: str, different_api_version: str = "", str_params: str = "", **dict_params: Dict) -> Any:
        full_path = self._build_full_path(path, different_api_version, str_params, **dict_params)
        return self._request_content(full_path)
