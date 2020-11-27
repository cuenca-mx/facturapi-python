from typing import ClassVar


class Resource:
    _client: ClassVar['facturapi.Client']  # type: ignore
    _endpoint: ClassVar[str]
