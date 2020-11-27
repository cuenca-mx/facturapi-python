from dataclasses import dataclass
from typing import List
from datetime import datetime
from uuid import UUID


@dataclass
class Customer:
    id: str
    legal_name: str
    tax_id: str


@dataclass
class Tax:
    rate: float
    type: str
    withholding: bool
    factor: str


@dataclass
class Product:
    id: str
    description: str
    product_key: int
    unit_key: str
    unit_name: str
    price: float
    tax_included: bool
    taxes: List[Tax]
    sku: str


@dataclass
class Item:
    quantity: int
    discount: int
    product: Product


@dataclass
class InvoiceRequest:
    id: str
    created_at: datetime
    livemode: bool
    verification_url: str
    status: str
    type: str
    cancellation_status: str
    customer: Customer
    total: float
    uuid: UUID
    use: str
    folio_number: int
    series: str
    payment_form: str
    payment_method: str
    currency: str
    exchange: int
    items: List[Item]