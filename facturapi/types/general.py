from typing import List, Optional

from pydantic import BaseModel

from .validators import sanitize_dict


class CustomerAddress(BaseModel):
    """Address of a customer.

    Attributes:
        street (str): Street.
        exterior (str): Exterior place number.
        interior (str): Interior place number.
        neighborhood (str): 'Colonia'.
        zip (str): Postal code.
        city (str): City.
        municipality (str): 'Municipio or Alcaldía'.
        state (str): State of the address.
        country (str): Country.

    """

    street: Optional[str]
    exterior: Optional[str]
    interior: Optional[str]
    neighborhood: Optional[str]
    zip: Optional[str]
    city: Optional[str]
    municipality: Optional[str]
    state: Optional[str]
    country: Optional[str]


class CustomerBasicInfo(BaseModel):
    """Customer's basic info"""

    id: str
    legal_name: str
    tax_id: str


class ItemPart(BaseModel):
    """Defines a part of an invoice item."""

    description: str
    product_key: str
    quantity: Optional[int] = 1
    sku: Optional[str]
    unit_price: Optional[float]
    customs_keys: Optional[List[str]]


class Namespace(BaseModel):
    """Namespace for spceial XML namespaces for an invoice."""

    prefix: Optional[str]
    uri: Optional[str]
    schema_location: Optional[str]


class ProductBasicInfo(BaseModel):
    """Product's basic info."""

    id: str
    unit_name: str
    description: str


class SanitizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)
