from typing import Union, Dict, Any
import requests
import time
import urllib

from apps.general.constants import HEADERS, REQUESTS_MAX_RETRIES


class ParserClient:
    @staticmethod
    def _build_full_path(
        base_path: str,
        path: str,
        api_version: str = None,
        str_params: str = None,
        dict_params: dict = None
    ) -> str:
        """
        It receives the path from path to make the get requests. It accepts url depending on
        the information required and extra_params that can vary from one url to another.
        """
        full_path = base_path
        if api_version:
            full_path = f"{full_path}{api_version}/"
        full_path = f"{full_path}{path}"
        if str_params:
            full_path = f"{path}/{str_params}"
        if dict_params:
            dict_params = urllib.parse.urlencode(dict_params)
            full_path = f'{full_path}&{dict_params}'
        return full_path

    @staticmethod
    def _request_content(
        full_url: str
    ) -> Union[Dict[str, Any], str, str, requests.Response]:
        """
        It performs a get request. full_url comes from _build_full_path.
        """
        for attempt in range(1, REQUESTS_MAX_RETRIES):
            response = requests.get(full_url, headers=HEADERS)
            if response.status_code == requests.codes.ok:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return response.json()
                if 'text/csv' in content_type:
                    return response.text
                if 'text/plain' in content_type:
                    return response.text
                else:
                    return response
            time.sleep(attempt * REQUESTS_MAX_RETRIES)
        response.raise_for_status()

    def request(
        self,
        base_path: str,
        path: str,
        api_version: str = None,
        str_params: str = None,
        dict_params: dict = None
    ) -> requests.Response:
        full_path = self._build_full_path(base_path, path, api_version, str_params, dict_params)
        return self._request_content(full_path)
