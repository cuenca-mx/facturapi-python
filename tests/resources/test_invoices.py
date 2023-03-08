import pytest

import facturapi
from facturapi.resources.customers import CustomerRequest
from facturapi.resources.invoices import InvoiceRequest
from facturapi.types import FileType, PaymentForm
from facturapi.types.exc import MultipleResultsFound, NoResultFound
from facturapi.types.general import CustomerAddress, ItemPart


@pytest.mark.vcr
def test_create_invoice():
    invoice_request = InvoiceRequest(
        customer=CustomerRequest(
            legal_name='Remedios Varo',
            tax_id='VAUR631216M55',
            email='remedios@varo.com',
            tax_system='625',
            address=CustomerAddress(
                street='Colima',
                exterior='196',
                interior='1',
                neighborhood='Roma',
                zip='06700',
                city='Ciudad de México',
                municipality='Cuauhtémoc',
                state='Ciudad de México',
            ),
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

    invoice_dict = invoice.to_dict()
    assert isinstance(invoice_dict, dict)
    assert invoice_dict['id']
    assert invoice_dict['created_at']
    assert invoice_dict['uuid']
    assert invoice_dict['items']


@pytest.mark.vcr
def test_retrieve_invoice():
    invoice_request = InvoiceRequest(
        customer='5fc5aa9938e6a2001b31aa21',
        items=[
            dict(
                product=dict(
                    description='Producto Test',
                    product_key='50202201',
                    price=42.05,
                ),
            ),
        ],
        payment_form=PaymentForm.tarjeta_de_credito,
    )
    invoice = facturapi.Invoice.create(data=invoice_request)
    retrieved_invoice = facturapi.Invoice.retrieve(id=invoice.id)

    assert retrieved_invoice.id == invoice.id
    assert retrieved_invoice.created_at == invoice.created_at
    assert retrieved_invoice.status == invoice.status
    assert retrieved_invoice.uuid == invoice.uuid


@pytest.mark.vcr
def test_cancel_invoice():
    invoice_id = '63fe4be4e87ce2001b19077f'
    invoice = facturapi.Invoice.retrieve(id=invoice_id)

    cancelled_invoice = facturapi.Invoice.cancel(
        invoice_id=invoice.id, motive='01'
    )

    assert cancelled_invoice.id == invoice.id
    assert cancelled_invoice.status != invoice.status

    invoice.refresh()
    assert cancelled_invoice.status == invoice.status
    assert cancelled_invoice.cancellation_status == 'accepted'
    assert invoice.cancellation_status == 'accepted'


@pytest.mark.vcr
def test_download_invoice():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(
        id=invoice_id, file_type=FileType.pdf
    )

    assert invoice_bytes
    assert type(invoice_bytes) == bytes


@pytest.mark.vcr
def test_download_invoice_xml():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(
        id=invoice_id, file_type=FileType.xml
    )

    assert invoice_bytes
    assert type(invoice_bytes) == bytes


@pytest.mark.vcr
def test_download_invoice_zip():
    invoice_id = 'INVOICE01'
    invoice_bytes = facturapi.Invoice.download(
        id=invoice_id, file_type=FileType.zip
    )

    assert invoice_bytes
    assert type(invoice_bytes) == bytes


@pytest.mark.vcr
def test_invoice_customer_property():
    invoice_id = 'INVOICE01'
    invoice = facturapi.Invoice.retrieve(id=invoice_id)
    assert invoice.id

    customer = invoice.customer
    assert customer.id == invoice.customer_info.id


@pytest.mark.vcr
def test_query_invoice_one():
    invoice = facturapi.Invoice.one()
    assert invoice.id


@pytest.mark.vcr
def test_query_invoice_one_multiple():
    with pytest.raises(MultipleResultsFound):
        _ = facturapi.Invoice.one()


@pytest.mark.vcr
def test_query_invoice_one_no_found():
    with pytest.raises(NoResultFound):
        _ = facturapi.Invoice.one(q='Cordelia Urueta Sierra')


@pytest.mark.vcr
def test_query_invoice_first():
    invoice = facturapi.Invoice.first()
    assert invoice is not None
    assert invoice.id


@pytest.mark.vcr
def test_query_invoice_first_none():
    invoice = facturapi.Invoice.first(q='Cordelia Urueta Sierra')
    assert invoice is None


@pytest.mark.vcr
def test_query_invoice_count():
    count = facturapi.Invoice.count()
    assert count == 1


@pytest.mark.vcr
def test_query_invoice_all():
    all_invoices = facturapi.Invoice.all(limit=1)

    for invoice in all_invoices:
        assert invoice.id
