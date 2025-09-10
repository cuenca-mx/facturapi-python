from dataclasses import dataclass
from typing import Any


class FacturapiException(Exception):
    pass


class NoResultFound(FacturapiException):
    """No results where found"""


class MultipleResultsFound(FacturapiException):
    """One result was expected but multiple were returned"""


@dataclass
class FacturapiResponseException(FacturapiException):
    json: dict[str, Any]
    status_code: int

    def __str__(self) -> str:
        return repr(self)
