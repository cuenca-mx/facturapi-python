import datetime as dt
from typing import ClassVar, Dict, List, Optional, Union, cast

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from ..types import InvoiceRelation, InvoiceUse, PaymentForm, PaymentMethod
from ..types.general import (
    CustomerBasicInfo,
    ItemPart,
    Namespace,
    ProductBasicInfo,
)
from .base import Creatable, Deletable, Downloadable, Queryable, Retrievable
from .customers import Customer, CustomerRequest
from .resources import retrieve_property


class InvoiceItem(BaseModel):
    quantity: Optional[int] = 1
    discount: Optional[float] = 0
    product: Union[
        str, ProductBasicInfo, Dict
    ]  # TO DO: Change Dict for ProductRequest
    custom_keys: Optional[List[str]]
    complement: Optional[str]
    parts: Optional[List[ItemPart]]
    property_tax_account: Optional[str]


class InvoiceRequest(BaseModel):
    """Model for a request to create an Invoice."""

    customer: Union[str, CustomerRequest]
    items: List[InvoiceItem]
    payment_form: PaymentForm
    payment_method: Optional[PaymentMethod] = PaymentMethod.contado
    use: Optional[InvoiceUse] = InvoiceUse.adquisicion_mercancias
    folio_number: Optional[int]
    series: Optional[str]
    currency: Optional[str] = 'MXN'
    exchange: Optional[float] = 1.0
    conditions: Optional[str]
    foreign_trade: Optional[Dict]
    related: Optional[List[str]]
    relation: Optional[InvoiceRelation]
    pdf_custom_section: Optional[str]
    addenda: Optional[str]
    namespaces: Optional[Namespace]


@dataclass
class Invoice(Creatable, Deletable, Downloadable, Queryable, Retrievable):
    """Invoice resource.

    Resource and data for an Invoice.

    """

    _resource: ClassVar = 'invoices'
    _relations: ClassVar = ['customer']

    created_at: dt.datetime
    livemode: bool
    status: str
    customer_info: CustomerBasicInfo
    customer_uri: str
    total: float
    uuid: str
    payment_form: PaymentForm
    items: List[InvoiceItem]
    currency: str
    exchange: float
    cancellation_status: Optional[str]
    folio_number: Optional[int]
    series: Optional[str] = None
    related: Optional[List[str]] = None
    relation: Optional[InvoiceRelation] = None

    @property
    def customer(self) -> Customer:
        """Fetch and access Customer resource.

        This property fetches and maps the customer
        related to an invoice so it can be accessed
        through a simple property instead of making a
        manual retrieve.

        Returns:
            Customer: Customer related to the invoice.

        """
        return cast(Customer, retrieve_property(self.customer_uri))

    @classmethod
    def create(cls, data: InvoiceRequest) -> 'Invoice':
        """Create an invoice.

        Args:
            data: All the request data to create an invoice.

        Returns:
            Invoice: The created resource.

        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)
        return cast('Invoice', cls._create(**cleaned_data))

    @classmethod
    def cancel(cls, invoice_id: str) -> 'Invoice':
        """Cancel an invoice.

        Calls a DELETE request on invoice resource.

        Args:
            invoice_id: The ID of the invoice to cancel.

        Returns:
            Invoice: The cancelled invoice resource.

        """
        return cast('Invoice', cls._delete(invoice_id))
