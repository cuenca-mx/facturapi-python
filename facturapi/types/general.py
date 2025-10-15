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

    street: str | None = None
    exterior: str | None = None
    interior: str | None = None
    neighborhood: str | None = None
    zip: str | None = None
    city: str | None = None
    municipality: str | None = None
    state: str | None = None
    country: str | None = None


class CustomerBasicInfo(BaseModel):
    """Customer's basic info"""

    id: str
    legal_name: str
    tax_id: str


class ItemPart(BaseModel):
    """Defines a part of an invoice item."""

    description: str
    product_key: str
    quantity: int | None = 1
    sku: str | None = None
    unit_price: float | None = None
    customs_keys: list[str] | None = None


class Namespace(BaseModel):
    """Namespace for spceial XML namespaces for an invoice."""

    prefix: str | None = None
    uri: str | None = None
    schema_location: str | None = None


class ProductBasicInfo(BaseModel):
    """Product's basic info."""

    id: str
    unit_name: str
    description: str


class SanitizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)
