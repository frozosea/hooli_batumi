import datetime
from typing import List
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Apartment:
    Id: int
    AddDate: datetime.datetime
    Images: List[str]
    Address: str
    UsdPrice: float
    Floor: int
    Description: str
    Square: int
    Url: str


@dataclass(unsafe_hash=True)
class AddTask:
    Url: str
    GroupId: int
