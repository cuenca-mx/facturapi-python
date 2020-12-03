import pytest


@pytest.fixture
def some_api_key(monkeypatch) -> None:
    monkeypatch.setenv('FACTURAPI_KEY', 'api_key')
