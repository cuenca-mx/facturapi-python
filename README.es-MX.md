<p align="center">
    <a href="https://facturapi.io">
        <img alt="Facturapi Logo" src="./docs/images/facturapi-logo.svg" width="200" />
    </a>
</p>
<h1 align="center">
    FacturAPI – Librería de Python
</h1>

![test](https://github.com/cuenca-mx/facturapi-python/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/cuenca-mx/facturapi-python/branch/main/graph/badge.svg?token=U89Q4PR339)](https://codecov.io/gh/cuenca-mx/facturapi-python)
[![PyPI version](https://badge.fury.io/py/facturapi.svg)](https://badge.fury.io/py/facturapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Esta es una librería de Python para https://www.facturapi.io

**⚠️Advertencia: Esta librería NO es oficial y aún sigue en desarrollo. No es un producto final.⚠️**

FacturAPI facilita la creación de facturas válidas para desarrolladores en México (Facturas Electrónicas o CFDI).

Esta librería está basada en [`cuenca-python`](https://github.com/cuenca-mx/cuenca-python) 💙.

## 💻 Instalación

Fácil, únicamente utiliza `pip` para instalar la librería:

```bash
pip install facturapi
```

## 🚀 Primeros pasos

### Autenticación con API Key
Asegurate de crear una cuenta gratis en [FacturAPI](https://www.facturapi.io) y tener acceso a tus llaves de test y live.

Hay dos formas de configurar tus llaves para usar la librería:

1. **Variable de entorno:** Configura una variable de entorno y la librería usará la llave automáticamente:

    ```bash
    export FACTURAPI_KEY=TU_API_KEY
    ```

2. **Usando el método `configure`:** Puedes configurar tu llave en el código usando el método `configure`:

    ```python
    from facturapi import configure

    configure(api_key='TU_API_KEY')
    ```

### Crea un Cliente
Después de configurar tu llave, puedes usar la librería para realizar varias acciones en los recursos de FacturAPI, por ejempo crear un Cliente:

```python
import facturapi
from facturapi.resources.customers import CustomerRequest, CustomerUpdateRequest

customer = facturapi.Customer.create(data=CustomerRequest(
    legal_name='Frida Kahlo',
    tax_id='ABCD111111CBA',
    email='frida_kahlo@test.com',
))
```

Para más detalles en los datos necesarios para crear un Cliente y otros recursos, revisa la [documentación](http://docs.facturapi.io).

Puedes encontrar más ejemplos de código de cómo crear y usar recursos en el directorio de [examples](./examples/). 

## 📚 Documentación

Encuentra más información de Facturapi y sus recursos en sus [docs](http://docs.facturapi.io).

O para más detalles técnicos y de la librería, entra a la [documentación](https://cuenca-mx.github.io/facturapi-python/) de `facturapi-python`.

## 💡 Contribuye
### ¿Encontraste un bug?
Crea un `issue` explicando el problema y cómo replicarlo.

### ¿Quieres contribuir?
Haz un `fork` del respositorio y crea tu PR, ¡toda la ayuda es bienvenida y apreciada!
No olvides mantener la cobertura del código arriba de 98%, nos encanta tener código testeado. 😋 

### Contactos:
- **Facturapi:** contacto@facturapi.io

- **Cuenca:** dev@cuenca.com

---
Desarrollado y mantenido con 💙 por [Cuenca](https://cuenca.com/)
<p align="center">
    <a href="https://cuenca.com/">
        <img alt="Cuenca Logo" src="./docs/images/cuenca-full-logo.svg" width="200" />
    </a>
</p>
