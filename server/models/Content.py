from dataclasses import dataclass
from models import Influencer, Place


@dataclass
class Content:
    id: str
    name: str
    sourceUrl: str
    place: Place
    influencer: Influencer
