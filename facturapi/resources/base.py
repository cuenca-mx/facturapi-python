from dataclasses import asdict, dataclass, fields
from typing import ClassVar, Dict, Generator, Optional, Union
from urllib.parse import urlencode

from ..exc import MultipleResultsFound, NoResultFound
from ..http import client


@dataclass
class Resource:
    _resource: ClassVar[str]

    id: str

    # purely for MyPy
    def __init__(self, **_):  # pragma: no cover
        ...

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Union[str, int]]) -> 'Resource':
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)

    @classmethod
    def _filter_excess_fields(
        cls, obj_dict: Dict[str, Union[str, int]]
    ) -> None:
        """
        dataclasses don't allow __init__ to be called with excess fields.
        This method allows the API to add fields in the response body without
        breaking the client.
        """
        excess = set(obj_dict.keys()) - {f.name for f in fields(cls)}
        for f in excess:
            del obj_dict[f]

    def to_dict(self):
        return asdict(self)


class Retrievalbe(Resource):
    @classmethod
    def retrieve(cls, id: str) -> Resource:
        response = client.get(f'/{cls._resource}/{id}')
        return cls._from_dict(response)

    def refresh(self):
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Creatable(Resource):
    @classmethod
    def create(cls, **data) -> Resource:
        response = client.post(cls._resource, data)
        return cls._from_dict(response)


class Updateable(Resource):
    @classmethod
    def update(cls, id: str, **data) -> Resource:
        response = client.put(f'/{cls._resource}/{id}', data)
        return cls._from_dict(response)


class Deletable(Resource):
    @classmethod
    def delete(cls, id: str) -> Resource:
        response = client.delete(f'/{cls._resource}/{id}')
        return cls._from_dict(response)


@dataclass
class Queryable(Resource):
    _query_params: ClassVar

    @classmethod
    def one(cls, **query_params) -> Resource:
        q = cls._query_params(limit=2, **query_params)
        response = client.get(cls._resource, q.dict())
        items = response['data']
        len_items = len(items)
        if not len_items:
            raise NoResultFound
        if len_items > 1:
            raise MultipleResultsFound
        return cls._from_dict(items[0])

    @classmethod
    def first(cls, **query_params) -> Optional[Resource]:
        q = cls._query_params(limit=1, **query_params)
        response = client.get(cls._resource, q.dict())
        try:
            item = response['data'][0]
        except IndexError:
            rv = None
        else:
            rv = cls._from_dict(item)
        return rv

    @classmethod
    def count(cls, **query_params) -> int:
        q = cls._query_params(**query_params)
        response = client.get(cls._resource, q.dict())
        items = response['data']
        return len(items)

    @classmethod
    def all(cls, **query_params) -> Generator[Resource, None, None]:
        q = cls._query_params(**query_params)
        next_page_uri = f'{cls._resource}?{urlencode(q.dict())}'
        current_page = 1
        while next_page_uri:
            page = client.get(next_page_uri)
            yield from (cls._from_dict(item) for item in page['data'])
            next_page_uri = ''
            if current_page < page['total_pages']:
                current_page += 1
                q.page = current_page
                next_page_uri = f'{cls._resource}?{urlencode(q.dict())}'
