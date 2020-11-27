import pytest

from facturapi.exc import FacturapiResponseException
from facturapi.http.client import Client


def test_auth_without_env():
    client = Client()
    assert not client.api_key


def test_auth_configure():
    client = Client()
    client.configure('api_key')
    assert client.api_key == 'api_key'


@pytest.mark.vcr
def test_invalid_auth():
    client = Client()
    with pytest.raises(FacturapiResponseException) as e:
        client.get('/invoices')
    assert e.value.status_code == 401
    assert str(e.value)


@pytest.mark.usefixtures('facturapi_creds')
def test_env_auth():
    client = Client()
    assert client.api_key == 'api_key'


@pytest.mark.usefixtures('facturapi_creds')
def test_override_with_configure():
    client = Client()
    client.configure('api_key2')
    assert client.api_key == 'api_key2'
