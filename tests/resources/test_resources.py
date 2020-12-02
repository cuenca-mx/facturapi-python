import pytest

from facturapi.resources.resources import retrieve_property


def test_retrieve_wrong_uri():
    with pytest.raises(ValueError):
        retrieve_property('wrong_uri')
