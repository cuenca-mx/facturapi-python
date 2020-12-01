import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types.general import CustomerAddress
from .base import Creatable, Retrievable


class CustomerRequest(BaseModel):
    legal_name: str
    tax_id: str
    email: str
    phone: Optional[str]
    address: Optional[CustomerAddress]


@dataclass
class Customer(Creatable, Retrievable):
    """Customer resource

    Resource and data for a Customer.

    """

    _resource: ClassVar = 'customers'

    created_at: dt.datetime
    livemode: bool
    legal_name: str
    tax_id: str
    email: str
    address: Optional[CustomerAddress]
    phone: Optional[str] = None

    @classmethod
    def create(cls, data: CustomerRequest) -> 'Customer':
        """Create a customer.

        Args:
            data: All the request data to create a customer.

        Returns:
            Customer: The created resource.

        """
        return cast('Customer', cls._create(**data.dict()))
