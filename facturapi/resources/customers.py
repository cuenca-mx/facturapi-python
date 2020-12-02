import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types.general import CustomerAddress
from .base import Creatable, Queryable, Retrievable, Updatable


class CustomerRequest(BaseModel):
    legal_name: str
    tax_id: str
    email: str
    phone: Optional[str]
    address: Optional[CustomerAddress]


class CustomerUpdateRequest(BaseModel):
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[CustomerAddress]


@dataclass
class Customer(Creatable, Queryable, Retrievable, Updatable):
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
            Customer: The created customer resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Customer', cls._create(**cleaned_data))

    @classmethod
    def update(cls, id: str, data: CustomerUpdateRequest) -> 'Customer':
        """Update a customer.

        Args:
            id: ID of the customer to be updated.
            data: Data to be updated.

        Returns:
            Customer: The udpated customer resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Customer', cls._update(id=id, **cleaned_data))
