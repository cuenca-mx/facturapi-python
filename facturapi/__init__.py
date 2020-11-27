__all__ = [
    '__version__',
    'configure',
]

from .http import client
from .version import __version__

configure = client.configure
