from dataclasses import dataclass
from typing import List


@dataclass(unsafe_hash=True)
class Appartment:
    Images: List[str]
    Address: str
    UsdPrice: float
    LariPrice: float
    Floor: str
    Description: str
    Square: int
    Benefits: List[str]
    Url: str
