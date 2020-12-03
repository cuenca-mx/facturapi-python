"""
Customer resource, it includes the class Resource and two request
classes to create and update the resource.

"""

import datetime as dt
from typing import ClassVar, Optional, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types.general import CustomerAddress
from .base import Creatable, Queryable, Retrievable, Updatable


class CustomerRequest(BaseModel):
    """
    This request must be filled to `create` a Customer.
    It contains all information necessary to create this resource.

    Attributes:
        legal_name (str): Full name of the customer.
        tax_id (str): RFC of the customer.
        email (str): Email of the customer.
        phone (str): Phone of the customer. Optional.
        address (CustomerAddress): Address object of the customer. Optional.

    """

    legal_name: str
    tax_id: str
    email: str
    phone: Optional[str]
    address: Optional[CustomerAddress]


class CustomerUpdateRequest(BaseModel):
    """
    This request must be filled to `update` a Customer.
    It contains all information necessary to update this resource.

    Attributes:
        legal_name (str): Full name of the customer. Optional.
        tax_id (str): RFC of the customer. Optional.
        email (str): Email of the customer. Optional.
        phone (str): Phone of the customer. Optional.
        address (CustomerAddress): Address object of the customer. Optional.

    """

    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[CustomerAddress]


@dataclass
class Customer(Creatable, Queryable, Retrievable, Updatable):
    """Customer resource

    Resource for a Customer. It inherits from `Creatable`, `Queryable`,
    `Retrievable` and `Updatable`.

    Attributes:
        created_at (datetime.datetime): The datetime in which the
            resource was created.
        livemode (bool): If the resource was created in test or live
            mode.
        legal_name (str): Name of the customer.
        tax_id (str): RFC of the customer.
        email (str): Email of the customer.
        address (CustomerAddress): Address data of the model. Optional.
        phone (str): Phone of the customer. Defaults to `None`.

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
