__all__ = [
    'Customer',
    'Invoice',
]

from .customers import Customer
from .invoices import Invoice
from .resources import RESOURCES

resource_classes = [
    Customer,
    Invoice,
]
for resource_cls in resource_classes:
    RESOURCES[resource_cls._resource] = resource_cls  # type: ignore
