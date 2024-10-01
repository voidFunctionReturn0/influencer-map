from dataclasses import dataclass
from typing import Set


@dataclass
class Place:
    id: str
    name: str
    googleRating: float
    googleUserRatingsTotal: int
    categories: Set[str]
    address: str
    centerLat: float
    centerLon: float
    phone: str
