import os
from typing import Any, Dict, MutableMapping, Optional, Union
from urllib.parse import urljoin

import httpx
from httpx import Response

from ..types.exc import FacturapiResponseException
from ..version import CLIENT_VERSION

API_HOST = 'www.facturapi.io/v2'


class Client:
    """Client to perform http requests to Facturapi.

    By default it inits and uses an `API_KEY` configured as
    an environment variable `FACTURAPI_KEY`, if the key
    is going to be set latter, the method `configure()`
    can be used.

    Attributes:
        host (str): Base URL to perform requests.
        client (httpx.Client): The httpx client used
            to perform requests.
        api_key (str): API KEY for Facturapi

    """

    host: str = API_HOST
    client: httpx.AsyncClient

    def __init__(self):
        self.client = httpx.AsyncClient()
        self.client.headers.update(
            {
                'User-Agent': f'facturapi-python/{CLIENT_VERSION}',
                'Content-Type': 'application/json',
            }
        )

        # Auth
        self.api_key = os.getenv('FACTURAPI_KEY', '')
        self.client.auth = httpx.BasicAuth(self.api_key, '')

    def configure(self, api_key: str):
        """Configure the http client.

        Import the client and configure it passing the `API_KEY`
        instead of configuring it as an environment variable.

        Args:
            api_key: Facturapi `API_KEY`

        """
        self.api_key = api_key
        self.client.auth = httpx.BasicAuth(self.api_key, '')

    async def get(
        self,
        endpoint: str,
        params: Union[None, bytes, MutableMapping[str, str]] = None,
    ) -> Dict[str, Any]:
        """Performs GET request to Facturapi."""
        return await self.request('get', endpoint, params=params)

    async def post(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Performs POST request to Facturapi."""
        return await self.request('post', endpoint, data=data)

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs PUT request to Facturapi."""
        return await self.request('put', endpoint, data=data)

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Performs DELETE request to Facturapi."""
        return await self.request('delete', endpoint)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Union[None, bytes, MutableMapping[str, str]] = None,
        data: Optional[Dict[str, Union[int, str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Performs a request to Facturapi.

        Given a `method` and `endpoint`, perform a request to
        Facturapi.

        Args:
            method: HTTP method of the request.
            endpoint: Endpoint to make the request to.
            params: URL encoded parameters. Defaults to `None`.
            data: JSON data to be sent. Defaults to `None`.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dict[str, Any]: JSON of the request's response.

        Raises:
            FacturapiResponseException: If response is not
                successful.

        """
        response = await self.client.request(
            method=method,
            url=('https://' + self.host + urljoin('/', endpoint)),
            json=data,
            params=params,
            **kwargs,
        )
        self._check_response(response)
        return response.json()

    async def download_request(
        self,
        endpoint: str,
        **kwargs,
    ) -> bytes:
        """Performs a GET request handling a file download.

        Args:
            endpoint: Endpoint to make the request to.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bytes: Bytes of the requested file.

        Raises:
            FacturapiResponseException: If response is not
                successful.

        """
        response = await self.client.request(
            method='GET',
            url=('https://' + self.host + urljoin('/', endpoint)),
            **kwargs,
        )
        self._check_response(response)
        return response.content

    @staticmethod
    def _check_response(response: Response):
        if not response.is_success:
            raise FacturapiResponseException(
                json=response.json(),
                status_code=response.status_code,
            )
