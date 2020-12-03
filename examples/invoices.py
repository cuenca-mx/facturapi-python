import facturapi
from facturapi import configure
from facturapi.resources.invoices import InvoiceRequest
from facturapi.types import FileType, PaymentForm
from facturapi.types.general import ItemPart

# Configure API KEY if not set in env variable
configure(api_key='my_secret_api_key')


def main():
    # Create an Invoice:
    #   First fill the request object and then create the resource
    invoice_request = InvoiceRequest(
        customer='58e93bd8e86eb318b0197456',  # Customer can be a CustomerRequest or its ID.
        items=[
            dict(
                product=dict(
                    description='Producto Test',
                    product_key='50202201',
                    price=42.05,
                ),
                quantity=2,
            ),
        ],
        payment_form=PaymentForm.tarjeta_de_credito,
    )

    invoice = facturapi.Invoice.create(data=invoice_request)
    # Resource is now created an can be used to access data or perform actions.
    total = invoice.total

    invoice_file = facturapi.Invoice.download(
        id=invoice.id, file_type=FileType.pdf
    )

    with open('my_invoice_file.pdf', 'wb') as f:
        f.write(invoice_file)

    # Refresh the resource in case an update happened somewhere:
    invoice.refresh()

    # Cancel an invoice:
    cancelled_invoice = facturapi.Invoice.cancel(invoice_id=invoice.id)
    status = cancelled_invoice.status

    # Perform a query to bring a list or an specific invoice:
    # Checkout full query details on the docs:
    #   https://docs.facturapi.io/?javascript#lista-de-facturas
    query_result = facturapi.Invoice.all(q='John Doe')
    for invoice in query_result:
        # Iterate throught query's result
        continue

    # Or just query for a unique result
    only_one = facturapi.Invoice.first(q='John Doe')


if __name__ == '__main__':
    main()
