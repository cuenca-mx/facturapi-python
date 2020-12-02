import datetime as dt
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Extra
from pydantic.types import ConstrainedInt

MAX_PAGE_SIZE = 50
MIN_PAGE = 1


class PageSize(ConstrainedInt):
    gt = 0
    le = MAX_PAGE_SIZE


class Page(ConstrainedInt):
    gt = MIN_PAGE


class DateFilter(BaseModel):
    """Model for a date filter query.

    Defines possible filters for date values.
    Only a few resources' query can be filtered
    through date. For more details check out the docs.

    Attributes:
        gt: Filter for greater than the given date.
        gte: Filter for greater than or equals to the
            given date.
        lt: Filter for lesser than the given date.
        lte: Filter for lesser than or equals to the
        given date.

    """

    gt: Optional[Union[str, dt.datetime]]
    gte: Optional[Union[str, dt.datetime]]
    lt: Optional[Union[str, dt.datetime]]
    lte: Optional[Union[str, dt.datetime]]


class BaseQuery(BaseModel):
    """Base query to query for resources.

    Defines all the possible arguments to query
    for a given resource.

    Attributes:
        q: Query text, its value may depend on what you are
            querying for. Check out Facturapi's docs for more
            details.
        limit: Max number of results thrown in a query.
            Defaults to 50, its maximum value.
        page: Number of page to query. Defaults to 1.
        date: Object of type `DateFilter` that can contain one
            or more date filters.

    """

    q: Optional[str]
    limit: Optional[PageSize] = PageSize(MAX_PAGE_SIZE)
    page: Optional[Page] = Page(MIN_PAGE)
    date: Optional[DateFilter]

    class Config:
        extra = Extra.forbid

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        d = super().dict(*args, **kwargs)
        return d
