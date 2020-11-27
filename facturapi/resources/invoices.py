import datetime as dt
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from ..types import UserValidationFile
from .base import Resource
from .user_verification_data import UserValidationData
from facturapi.models.invoice_request import InvoiceRequest



@dataclass
class Invoice(Resource):
    """
    Based on: https://docs.facturapi.io/?shell#objeto-factura
    """

    _endpoint: ClassVar[str] = '/invoices'
    InvoiceResponse: Dict[str, Any]

    @classmethod
    def create(cls, invoice_request: InvoiceRequest) -> 'Invoice':
        data = invoice_request.to_dict()
        response = cls._client.post(cls._endpoint, json=data)
        return cls(**response)

