import pytest


@pytest.fixture(scope='module')
def vcr_config():
    config = dict(
        filter_headers=[('Authorization', 'DUMMY')],
        record_mode='once',
    )
    return config
