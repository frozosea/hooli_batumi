from dataclasses import dataclass
from typing import List


@dataclass()
class Apartment:
    Images: List[str]
    Address: str
    BedroomQuantity: int
    RoomQuantity: int
    UsdPrice: float
    Floor: str
    Square: int
