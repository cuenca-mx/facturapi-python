from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra
from pydantic.types import ConstrainedInt

MAX_PAGE_SIZE = 50
MIN_PAGE = 1


class PageSize(ConstrainedInt):
    gt = 0
    le = MAX_PAGE_SIZE


class Page(ConstrainedInt):
    gt = MIN_PAGE


class BaseQuery(BaseModel):
    q: str
    limit: Optional[PageSize] = PageSize(MAX_PAGE_SIZE)
    page: Optional[Page] = Page(MIN_PAGE)

    class Config:
        extra = Extra.forbid

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('exclude_unset', True)
        d = super().dict(*args, **kwargs)
        return d
