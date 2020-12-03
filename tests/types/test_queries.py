import pytest
from pydantic.error_wrappers import ValidationError

from facturapi.types import BaseQuery


def test_base_query():
    q = BaseQuery(q='Frida')
    assert q.dict() == dict(q='Frida')


def test_base_query_page_size():
    with pytest.raises(ValidationError):
        _ = BaseQuery(q='Frida', limit=51)


def test_base_query_page_min():
    with pytest.raises(ValidationError):
        _ = BaseQuery(q='Frida', page=0)
