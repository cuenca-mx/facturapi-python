<p align="center">
    <a href="https://facturapi.io">
        <img alt="Facturapi Logo" src="./docs/images/facturapi-logo.svg" width="200" />
    </a>
</p>
<h1 align="center">
    FacturAPI – Python Client Library
</h1>

![test](https://github.com/cuenca-mx/facturapi-python/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/cuenca-mx/facturapi-python/branch/main/graph/badge.svg?token=U89Q4PR339)](https://codecov.io/gh/cuenca-mx/facturapi-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Español](./README.es-MX.md)

This is a Python library for [FacturAPI](https://www.facturapi.io)

FacturAPI makes it easy for developers to generate valid Invoices in Mexico (known as Factura Electrónica or CFDI).

## 💻 Installation

## 🚀 Getting started

### Authenticate with your API Key
Be sure to create a free account on [FacturAPI](https://www.facturapi.io) and have access to your test or live API keys.

There are two ways to configure your API Key to use the library:

1. **Environment variable:** Just set an environment variable and the library will automatically use it:
   
   ```bash
   export FACTURAPI_KEY=YOUR_API_KEY
   ```

2. **Using the `configure` method:** If you want to set it in the code, you can import and use the `configure` method:

    ```python
    from facturapi import configure
    
    configure(api_key='YOUR_API_KEY')
    ```

### Create a customer
After configuring the API Key, you can use the client to perform many actions on the resources, for example to create
a Customer:

```python
import facturapi
from facturapi.resources.customers import CustomerRequest, CustomerUpdateRequest

customer = facturapi.Customer.create(data=CustomerRequest(
    legal_name='Frida Kahlo',
    tax_id='ABCD111111CBA',
    email='frida_kahlo@test.com',
))
```

For more details on the data used to create a Customer and other resources, be sure to check out the [docs](http://docs.facturapi.io).

More examples can be found on the [examples](./examples/) directory.

## 📚 Documentation
To find more documentation and use cases about the library and Facturapi, check out the [docs](http://docs.facturapi.io).
## 💡 Contribute
### Found a bug?
Please create an issue addressing the bug and how to replicate it.
### Want to contribute?
Be sure to fork the repo and send your PR! Any and all help is appreciated.
### Contacts:
- **Facturapi:** contacto@facturapi.io

- **Cuenca:** dev@cuenca.com

---
Developed and maintained with 💙 by [Cuenca](https://github.com/cuenca-mx)
<p align="center">
    <a href="https://cuenca.com/">
        <img alt="Cuenca Logo" src="./docs/images/cuenca-full-logo.svg" width="200" />
    </a>
</p>
