from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List


@dataclass(unsafe_hash=True)
class Message:
    message: str
    url: str
    user_url: str
    date: datetime.datetime
    images: List[str]





@dataclass
class Category:
    GroupId: str | int | float
    Eval: str
