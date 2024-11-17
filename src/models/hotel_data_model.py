from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str
    country: str

@dataclass
class Image:
    link: str
    description: str

@dataclass
class Amenities:
    general: List[str]
    room: List[str]

@dataclass
class Images:
    rooms: List[Image] = field(default_factory=list)
    site: List[Image] = field(default_factory=list)
    amenities: List[Image] = field(default_factory=list)

@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    location: Location
    description: Optional[str] = None
    amenities: Optional[Amenities] = None
    images: Optional[Images] = None
    booking_conditions: Optional[List[str]] = field(default_factory=list)
