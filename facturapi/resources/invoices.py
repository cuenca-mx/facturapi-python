import datetime as dt
from typing import ClassVar, Dict, List

from pydantic.dataclasses import dataclass

from .base import Creatable, Deletable, Queryable, Retrievable, Updateable


@dataclass
class Invoice(Retrievable, Creatable, Updateable, Deletable, Queryable):
    _resource: ClassVar = 'invoices'

    created_at: dt.datetime
    livemode: bool
    status: str
    cancellation_status: str
    customer: Dict[str, str]
    total: float
    uuid: str
    folio_number: int
    series: str
    payment_form: str
    items: List[Dict]
    related: List[str]
    relation: str
    currency: str
    exchange: float
