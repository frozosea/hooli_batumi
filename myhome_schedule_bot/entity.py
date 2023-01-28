import datetime

from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class LastAppartment:
    Id: int
    AddDate: datetime.datetime
    Url: str
