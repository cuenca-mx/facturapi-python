import facturapi
from facturapi.resources.customers import (
    CustomerRequest,
    CustomerUpdateRequest,
)


def main():
    # Create a customer by filling a CustomerRequest
    customer_request = CustomerRequest(
        legal_name='John Doe',
        tax_id='ABCD111111CBA',
        email='email@example.com',
    )
    customer = facturapi.Customer.create(data=customer_request)

    # Access to data or perform updates
    tax_id = customer.tax_id

    update_request = CustomerUpdateRequest(email='email2@example.net')
    updated_customer = facturapi.Customer.update(
        id=customer.id, data=update_request
    )

    assert updated_customer.email != customer.email

    # Retrieve customer by ID
    retrieved_customer = facturapi.Customer.retrieve('some_id')

    # Perform queries to retrieve by specific values:
    lots_of_customers = facturapi.Customer.all(limit=20)
    for customer in lots_of_customers:
        # Iterate through results and use them as resources:
        c_id = customer.id
        name = customer.name


if __name__ == '__main__':
    main()
