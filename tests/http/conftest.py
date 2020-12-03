import pytest


@pytest.fixture
def facturapi_creds(monkeypatch) -> None:
    monkeypatch.setenv('FACTURAPI_KEY', 'some_api_key')
