"""
Invoice resource, it includes the class Resource, a request
class to create the resource and a class to represent an
Invoice Item.

"""

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
    """
    Class representing an Item from an Invoice.

    Attributes:
        quantity (str): Number of items of this type. Defaults
            to `1`.
        discount (float): Discount on the item price if any.
            Defaults to `0`.
        product (Union[str, ProductBasicInfo, Dict]): Product
            ID, info or request to create a resource.
        custom_keys (List[str]): List of custom product keys.
            Optional.
        complement (str): XML code with additional info to add
            to the invoice. Optional.
        parts (List[ItemParts]): If the concept includes parts.
            Optional.
        property_tax_account (str): 'Predial' number. Optional.

    """

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
    """
    This request must be filled to `create` an Invoice.
    It contains all information necessary to create this resource.

    Attributes:
        customer (Union[str, CustomerRequest]): Customer ID or a
            CustomerRequest to create a new one.
        items (List[InvoiceItem]): List of items of the invoice.
        payment_form (PaymentForm): Form of payment.
        payment_method (PaymentMethod): Method of payment. Defaults
            to `PaymentMethod.contado`.
        use (InvoiceUse): Invoice SAT CFDI use. Defaults to
            `InvoiceUse.adquisicion_mercancias`.
        folio_number (int): Internal folio number. Optional.
        series (str): Internal series string. Optional.
        currency (str): Currency of the invoice in ISO format.
            Defaults to `MXN`.
        exchange (float): If a currency is present, the exchange
            value to Mexican Pesos. Defaults to `1.0`.
        conditions (str): Payment conditions. Optional.
        foreign_trade (Dict): Info to add a 'Complemento de Comercio
            Exterior'. Optional.
        related (List[str]): UUID list of related invoices. Optional.
        relation (InvoiceRelation): If related invoices are given,
            their relation key from the SAT catalogue. Optional.
        pdf_custom_section (str): HTML string code to include content
            to the invoice's PDF. Optional
        addenda (str): XML code with Addenda. Optional.
        namespaces (List[Namespace]): If `addenda` or an item complement
            is given, the special namespaces of the XML code. Optional.

    """

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
    """Invoice resource

    Resource for an Invoice. It inherits from `Creatable`, `Deletable`,
    `Downloadable`, `Queryable` and `Retrievable`.

    Attributes:
        created_at (datetime.datetime): The datetime in which the
            resource was created.
        livemode (bool): If the resource was created in test or live
            mode.
        status (str): Status of the invoice.
        customer_info (CustomerBasicInfo): Basic info of the Customer.
        customer_uri (str): URI representing how to fetch a Customer
            resource related to the Invoice.
        total (float): Invoice total.
        uuid (str): 'Folio fiscal' assigned by SAT.
        payment_form (PaymentForm): Form of payment of the Invoice.
        items (List[InvoiceItem]): List of items of the Invoice.
        currency (str): Currency of the invoice in ISO format.
        exchange (float): Exchange value to Mexican Pesos.
        cancellation_status (str): If the Invoice was cancelled, the
            status of the cancellation. Optional.
        folio_number (int): Folio number. Optional.
        series (str): Custom series string. Optional. Defaults to `None`.
        related (List[str]): UUID of related invoices. Defaults to
            `None`.
        relation (InvoiceRelation): Relation key from the SAT catalogue.
            Defaults to `None`.

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
