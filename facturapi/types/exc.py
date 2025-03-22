from dataclasses import dataclass
from typing import Any, Dict


class FacturapiException(Exception):
    ...


class NoResultFound(FacturapiException):
    """No results where found"""


class MultipleResultsFound(FacturapiException):
    """One result was expected but multiple were returned"""


@dataclass
class FacturapiResponseException(FacturapiException):
    json: Dict[str, Any]
    status_code: int

    def __str__(self) -> str:
        return repr(self)
