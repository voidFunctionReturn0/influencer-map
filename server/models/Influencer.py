from dataclasses import dataclass
from Constants import Platform


@dataclass
class Influencer:
    id: str
    name: str
    platform: Platform
    profileImage: str
