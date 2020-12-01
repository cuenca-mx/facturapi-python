import pytest

import facturapi
from facturapi.resources.invoices import InvoiceRequest
from facturapi.types import PaymentForm
from facturapi.types.general import ItemPart


@pytest.mark.vcr
def test_create_invoice():
    invoice_request = InvoiceRequest(
        customer=dict(  # TO DO: Use CustomerRequest
            legal_name='Remedios Varo',
            tax_id='VAUR631216M55',
            email='remedios@varo.com',
        ),
        items=[
            dict(
                product=dict(
                    description='Producto Test',
                    product_key='50202201',
                    price=42.05,
                ),
                quantity=2,
                discount=0.1,
                custom_keys=['Custom key'],
                parts=[
                    ItemPart(
                        description='Parte 1',
                        product_key='50202201',
                    )
                ],
            ),
        ],
        payment_form=PaymentForm.tarjeta_de_credito,
    )

    invoice = facturapi.Invoice.create(data=invoice_request)
    assert invoice.id
    assert invoice.created_at
    assert invoice.status
    assert invoice.uuid
    assert invoice.items


@pytest.mark.vcr
def test_retrieve_invoice():
    invoice_id = 'INVOICE01'
    invoice = facturapi.Invoice.retrieve(id=invoice_id)

    assert invoice_id == invoice.id
    assert invoice.created_at
    assert invoice.status
    assert invoice.uuid
    assert invoice.items

    status_before_refresh = invoice.status
    invoice.refresh()

    assert status_before_refresh == invoice.status


@pytest.mark.vcr
def test_cancel_invoice():
    invoice_id = 'INVOICE01'
    invoice = facturapi.Invoice.cancel(invoice_id=invoice_id)

    assert invoice_id == invoice.id
    assert invoice.cancellation_status == 'accepted'
    assert invoice.status == 'canceled'


@pytest.mark.vcr
def test_download_invoice():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(id=invoice_id, file_type='pdf')

    assert invoice_bytes
    assert type(invoice_bytes) == bytes


@pytest.mark.vcr
def test_download_invoice_xml():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(id=invoice_id, file_type='xml')

    assert invoice_bytes
    assert type(invoice_bytes) == bytes


@pytest.mark.vcr
def test_download_invoice_zip():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(id=invoice_id, file_type='zip')

    assert invoice_bytes
    assert type(invoice_bytes) == bytes
