from typing import List, Optional

from pydantic import BaseModel

from .validators import sanitize_dict


class CustomerAddress(BaseModel):
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
    id: str
    legal_name: str
    tax_id: str


class ItemPart(BaseModel):
    description: str
    product_key: str
    quantity: Optional[int] = 1
    sku: Optional[str]
    unit_price: Optional[float]
    customs_keys: Optional[List[str]]


class Namespace(BaseModel):
    prefix: Optional[str]
    uri: Optional[str]
    schema_location: Optional[str]


class ProductBasicInfo(BaseModel):
    id: str
    unit_name: str
    description: str


class SanitizedDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sanitize_dict(self)
