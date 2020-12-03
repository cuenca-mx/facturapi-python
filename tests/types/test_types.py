import datetime as dt
from enum import Enum

from pydantic.dataclasses import dataclass

from facturapi.types.general import SanitizedDict


class TEnum(Enum):
    zero = 0


@dataclass
class TClass:
    ein: int

    def to_dict(self):
        return dict(ein=self.ein, zwei='dos')


def test_sinitized_dict():
    now = dt.datetime.now()
    utc_now = now.astimezone(dt.timezone.utc)

    utc_date = dt.datetime.now(dt.timezone.utc)

    class_with_dict = TClass(ein=1)

    assert SanitizedDict(
        date=now,
        hello='there',
        many_numbers=class_with_dict,
        number=TEnum.zero,
        utc_date=utc_date,
    ) == dict(
        date=utc_now.isoformat(),
        hello='there',
        many_numbers=dict(
            ein=1,
            zwei='dos',
        ),
        number=0,
        utc_date=utc_date.isoformat(),
    )
