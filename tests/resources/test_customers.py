import pytest

import facturapi
from facturapi.resources.customers import (
    CustomerRequest,
    CustomerUpdateRequest,
)
from facturapi.types.exc import MultipleResultsFound, NoResultFound
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

    customer_dict = customer.to_dict()
    assert isinstance(customer_dict, dict)
    assert customer_dict['id']
    assert customer_dict['created_at']
    assert customer_dict['legal_name']
    assert customer_dict['tax_id']
    assert customer_dict['email']


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


@pytest.mark.vcr
def test_update_customer():
    customer_id = 'CUSTOMER01'
    customer = facturapi.Customer.retrieve(id=customer_id)

    email = customer.email
    update_data = CustomerUpdateRequest(email='remedios@pintora.com')

    updated_customer = facturapi.Customer.update(
        id=customer_id, data=update_data
    )
    assert updated_customer.email != email
    assert updated_customer.email == 'remedios@pintora.com'


@pytest.mark.vcr
def test_query_customer_one():
    customer = facturapi.Customer.one(q='Remedios')
    assert customer.id


@pytest.mark.vcr
def test_query_customer_one_multiple():
    with pytest.raises(MultipleResultsFound):
        _ = facturapi.Customer.one()


@pytest.mark.vcr
def test_query_customer_one_no_found():
    with pytest.raises(NoResultFound):
        _ = facturapi.Customer.one(q='Diego Rivera')


@pytest.mark.vcr
def test_query_customer_first():
    customer = facturapi.Customer.first()
    assert customer is not None
    assert customer.id


@pytest.mark.vcr
def test_query_customer_first_none():
    customer = facturapi.Customer.first(q='Diego Rivera')
    assert customer is None


@pytest.mark.vcr
def test_query_customer_count():
    count = facturapi.Customer.count()
    assert count == 2


@pytest.mark.vcr
def test_query_customer_all():
    all_customers = facturapi.Customer.all()

    for customer in all_customers:
        assert customer.id
