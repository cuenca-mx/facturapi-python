import datetime as dt
from typing import Annotated, Any

from pydantic import BaseModel, Field

MAX_PAGE_SIZE = 50
MIN_PAGE = 1

PageSize = Annotated[int, Field(gt=0, le=MAX_PAGE_SIZE)]
Page = Annotated[int, Field(ge=MIN_PAGE)]


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

    gt: str | dt.datetime | None = None
    gte: str | dt.datetime | None = None
    lt: str | dt.datetime | None = None
    lte: str | dt.datetime | None = None


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

    q: str | None = None
    limit: PageSize | None = PageSize(MAX_PAGE_SIZE)
    page: Page | None = Page(MIN_PAGE)
    date: DateFilter | None = None

    model_config = {"extra": "forbid"}

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        d = super().model_dump(*args, **kwargs)
        return d


class InvoiceQuery(BaseQuery):
    motive: str | None = None
