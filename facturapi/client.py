import os
from typing import Any, ClassVar, Dict, Optional

from requests import Response, Session
from requests.auth import HTTPBasicAuth

from .resources import Invoice
from .version import __version__ as client_version

API_URL = 'https://www.facturapi.io/v1/'


class Client:
    base_url: ClassVar[str] = API_URL
    headers: Dict[str, str]
    session: Session

    # resources
    invoice: ClassVar = Invoice

    def __init__(self):
        self.session = Session()

        # basic auth
        api_key = os.getenv('FACTURAPI_KEY', '')
        self.basic_auth = (api_key, '')

        self.headers = {
            'User-Agent': f'facturapi/{client_version}',
            'Content-Type': 'application/json',
        }
        Resource._client = self

    def get(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('get', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        return self.request('post', endpoint, **kwargs)

    def request(
        self, method: str, endpoint: str, **kwargs: Any,
    ) -> Dict[str, Any]:
        url = self.base_url + self.environment + endpoint
        headers = self.headers
        response = self.session.request(
            method, url, headers=headers, **kwargs
        )
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            return
        response.raise_for_status()
