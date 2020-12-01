import pytest

import facturapi
from facturapi.resources.customers import CustomerRequest
from facturapi.types.general import CustomerAddress


@pytest.mark.vcr
def test_create_customer():
    customer_request = CustomerRequest(
        legal_name='Cordelia Urueta Sierra',
        tax_id='UUSC9509162G7',
        email='cordelia@urueta.com',
        phone='5511223344',
        address=CustomerAddress(
            street='Colima',
            exterior='196',
            interior='1',
            neighborhood='Roma',
            zip='06700',
            city='Ciudad de México',
            municipality='Cuauhtémoc',
            state='Ciudad de México',
            country='México',
        ),
    )

    customer = facturapi.Customer.create(data=customer_request)
    assert customer.id
    assert customer.created_at
    assert customer.legal_name
    assert customer.tax_id
    assert customer.email


@pytest.mark.vcr
def test_retrieve_customer():
    customer_id = 'CUSTOMER01'
    customer = facturapi.Customer.retrieve(id=customer_id)

    assert customer_id == customer.id
    assert customer.created_at
    assert customer.legal_name
    assert customer.tax_id

    tax_id_before_refresh = customer.tax_id
    customer.refresh()

    assert tax_id_before_refresh == customer.tax_id
