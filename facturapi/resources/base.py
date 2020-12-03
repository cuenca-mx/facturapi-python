"""Base module for resources.

This module represent all the base code for resources,
the resources can inherit behaviour from these classes to
perform requests and actions to the API.
"""

from dataclasses import asdict, fields
from typing import Any, ClassVar, Dict, Generator, List, Optional
from urllib.parse import urlencode

from pydantic.dataclasses import dataclass

from ..http import client
from ..types import BaseQuery, FileType
from ..types.exc import MultipleResultsFound, NoResultFound
from ..types.general import SanitizedDict


@dataclass
class Resource:
    """Generic resource from Facturapi.

    Generic Resource class used by Facturapi resources.

    Attributes:
        _resource (ClassVar[str]): Name of the resource the
            class corresponds to.
        id (str): ID of the resource.

    """

    _resource: ClassVar[str]
    _relations: ClassVar[List[str]] = []

    id: str

    # purely for MyPy
    def __init__(self, **_):  # pragma: no cover
        ...

    @classmethod
    def _from_dict(cls, obj_dict: Dict[str, Any]) -> 'Resource':
        cls._filter_excess_fields(obj_dict)
        return cls(**obj_dict)

    @classmethod
    def _filter_excess_fields(cls, obj_dict: Dict[str, Any]) -> None:
        """
        dataclasses don't allow __init__ to be called with excess fields.
        This method allows the API to add fields in the response body without
        breaking the client.
        Also if data of a relation is found, the data is rearranged so the
        library can map relations easier.

        """
        excess = set(obj_dict.keys()) - {f.name for f in fields(cls)}
        for f in excess:
            if f in cls._relations:
                id_ = obj_dict[f]['id']
                obj_dict[f'{f}_uri'] = f'{f}s/{id_}'
                obj_dict[f'{f}_info'] = obj_dict[f]
            del obj_dict[f]

    def to_dict(self) -> Dict:
        return asdict(self, dict_factory=SanitizedDict)


class Retrievable(Resource):
    """Generic Retrievable class.

    Used by resources that can be retrieved, i.e: resources that can
    be retrieved by a GET request to its ID.

    """

    @classmethod
    def retrieve(cls, id: str) -> Resource:
        """Retrieve a resource given its ID

        Performs a GET request with the ID.

        Args:
            id: The ID of the resource

        Returns:
            Resource: The resource retrieved.

        """
        response = client.get(f'/{cls._resource}/{id}')
        return cls._from_dict(response)

    def refresh(self):
        """Refresh a resource

        Refresh resource's data to be sure its the latest. It
        performs a GET request on the resource.

        Returns:
            Resource: The refreshed resource.

        """
        new = self.retrieve(self.id)
        for attr, value in new.__dict__.items():
            setattr(self, attr, value)


class Downloadable(Resource):
    """Generic Downloadable class.

    Used by resources that can be downloaded as a file.

    """

    @classmethod
    def download(cls, id: str, file_type: FileType) -> bytes:
        """Download a file from resource.

        Performs a GET request to download a file given a
        resource ID.

        Args:
            id: The ID of the resource.
            file_type: Type of the file to be downloaded.
                (zip, pdf or xml).

        Returns:
            bytes: Bytes of the file.

        """
        return client.download_request(
            f'/{cls._resource}/{id}/{file_type.value}'
        )


class Creatable(Resource):
    """Generic Creatable class.

    Used by resources that can be created.

    """

    @classmethod
    def _create(cls, **data) -> Resource:
        """Create a resource

        Performs a POST request with the data.

        Args:
            data (dict): Data from the resource to create.

        Returns:
            Resource: The created resource.

        """
        response = client.post(cls._resource, data)
        return cls._from_dict(response)


class Updatable(Resource):
    """Generic Updatable class.

    Used by resources that can be updated.

    """

    @classmethod
    def _update(cls, id: str, **data) -> Resource:
        """Update an specific resource with new data.

        Performs a PUT request with the updated data.

        Args:
            id: The ID of the resource.

        Returns:
            Resource: The updated resource.

        """
        response = client.put(f'/{cls._resource}/{id}', data)
        return cls._from_dict(response)


class Deletable(Resource):
    """Generic Deletable class.

    Used by resources that can be deleted.

    """

    @classmethod
    def _delete(cls, id: str) -> Resource:
        """Delete an specific resource.

        Performs a DELETE request on the ID.

        Args:
            id: The ID of the resource to delete.

        Returns:
            Resource: The deleted resource.

        """
        response = client.delete(f'/{cls._resource}/{id}')
        return cls._from_dict(response)


@dataclass
class Queryable(Resource):
    """Generic Queryable class.

    Used by resources that can be queried in lists. Refer to this
    class to see the query actions that can be performed on a
    resource.

    Attributes:
        _query_params: A class with the parameters that
            can be queried.
    """

    _query_params: ClassVar = BaseQuery

    @classmethod
    def one(cls, **query_params) -> Resource:
        """Retrieve only one resource given a query.

        Given a query, retrieve one and only one resource. If more
        than one resource or none are found, this method throws an
        exception.

        Args:
            **query_params (dict): Arbitrary query keyword arguments.

        Raises:
            NoResultFound: If no result is found.
            MultipleResultsFound: If more than one result is found.

        Returns:
            Resource: The one resource queried.

        """
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
        """Retrieve the first resource found given a query or none.

        Args:
            **query_params (dict): Arbitrary query keyword arguments.

        Returns:
            Optional[Resource]: The first resource queried or `None`
                if none found.

        """
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
        """Get the total number of results given a query.

        Args:
            **query_params (dict): Arbitrary query keyword arguments.

        Returns:
            int: The total count of results.

        """
        q = cls._query_params(**query_params)
        response = client.get(cls._resource, q.dict())
        items = response['data']
        return len(items)

    @classmethod
    def all(cls, **query_params) -> Generator[Resource, None, None]:
        """Retrieve all resources given a query.

        All the returned resources are paginated, the method `yields`
        the first page of results and if more are found; then it
        continues to `yield` pages until all results are queried.

        Args:
            **query_params (dict): Arbitrary query keyword arguments.

        Returns:
            Generator: A generator containing the queried results.

        """
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
