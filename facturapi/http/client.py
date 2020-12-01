import os
from typing import Any, Dict, MutableMapping, Optional, Union, cast
from urllib.parse import urljoin

import requests
from requests import Response

from ..types.exc import FacturapiResponseException
from ..version import CLIENT_VERSION

API_HOST = 'www.facturapi.io/v1'


class Client:
    """Client to perform http requests to Facturapi.

    By default it inits and uses an `API_KEY` configured as
    an environment variable `FACTURAPI_KEY`, if the key
    is going to be set latter, the method `configure()`
    can be used.

    Attributes:
        host (str): Base URL to perform requests.
        session (requests.Session): The requests session used
            to perform requests.
        api_key (str): API KEY for Facturapi

    """

    host: str = API_HOST
    session: requests.Session

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': f'facturapi-python/{CLIENT_VERSION}',
                'Content-Type': 'application/json',
            }
        )

        # Auth
        self.api_key = os.getenv('FACTURAPI_KEY', '')
        self.session.auth = (self.api_key, '')

    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_data = {}
        for k, v in data.items():
            if isinstance(v, list):
                for i, c in enumerate(v):
                    if isinstance(c, dict):
                        v[i] = self._clean_data(c)
                    elif c is None:
                        v.pop(i)
                cleaned_data[k] = cast(Any, v)
            elif isinstance(v, dict):
                cleaned_data[k] = dict(**self._clean_data(v))
            elif v is not None:
                cleaned_data[k] = v
        return cleaned_data

    def configure(self, api_key: str):
        """Configure the http client.

        Import the client and configure it passing the `API_KEY`
        instead of configuring it as an environment variable.

        Args:
            api_key: Facturapi `API_KEY`

        """
        self.api_key = api_key
        self.session.auth = (self.api_key, '')

    def get(
        self,
        endpoint: str,
        params: Union[None, bytes, MutableMapping[str, str]] = None,
    ) -> Dict[str, Any]:
        """Performs GET request to Facturapi"""
        return self.request('get', endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs POST request to Facturapi"""
        return self.request('post', endpoint, data=data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs PUT request to Facturapi"""
        return self.request('put', endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Performs DELETE request to Facturapi"""
        return self.request('delete', endpoint)

    def request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data: Optional[Dict[str, Union[int, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Performs a request to Facturapi.

        Given a `method` and `endpoint`, perform a request to
        Facturapi.

        Args:
            method: HTTP method of the request.
            endpoint: Endpoint to make the request to.
            params:
            data:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dict[str, Any]: JSON of the request's response.

        Raises:
            FacturapiResponseException: If response is not
                successful.

        """
        if data:
            data = self._clean_data(data)

        response = self.session.request(
            method=method,
            url=('https://' + self.host + urljoin('/', endpoint)),
            json=data,
            params=params,
            **kwargs,
        )
        self._check_response(response)
        return response.json()

    @staticmethod
    def _check_response(response: Response):
        if response.ok:
            return
        raise FacturapiResponseException(
            json=response.json(),
            status_code=response.status_code,
        )
