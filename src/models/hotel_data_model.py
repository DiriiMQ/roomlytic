from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    def _export_dict(self) -> dict:
        return {
            "lat": self.lat,
            "lng": self.lng,
            "address": self.address,
            "city": self.city,
            "country": self.country
        }

@dataclass
class Image:
    link: Optional[str] = None
    description: Optional[str] = None

    def _export_dict(self) -> dict:
        return {
            "link": self.link,
            "description": self.description
        }

@dataclass
class Amenities:
    general: Optional[List[str]] = field(default_factory=list)
    room: Optional[List[str]] = field(default_factory=list)

    def _export_dict(self) -> dict:
        return {
            "general": self.general,
            "room": self.room
        }

@dataclass
class Images:
    rooms: Optional[List[Image]] = field(default_factory=list)
    site: Optional[List[Image]] = field(default_factory=list)
    amenities: Optional[List[Image]] = field(default_factory=list)

    def _import(self, data: dict) -> "Images":
        self.rooms = [Image(**room) for room in data.get("rooms")]
        self.site = [Image(**site) for site in data.get("site")]
        self.amenities = [Image(**amenity) for amenity in data.get("amenities")]

        return self
    
    def _export_dict(self) -> dict:
        return {
            "rooms": [room._export_dict() for room in self.rooms],
            "site": [site._export_dict() for site in self.site],
            "amenities": [amenity._export_dict() for amenity in self.amenities]
        }
    

@dataclass
class Hotel:
    id: str = ""
    destination_id: str = ""
    name: str = ""
    location: Optional[Location] = Location()
    description: Optional[str] = None
    amenities: Optional[Amenities] = Amenities()
    images: Optional[Images] = Images()
    booking_conditions: Optional[List[str]] = field(default_factory=list)

    def _import(self, data: dict) -> "Hotel":
        self.id = data.get("id")
        self.destination_id = str(data.get("destination_id"))
        self.name = data.get("name")
        self.location = Location(**data.get("location"))
        self.description = data.get("description")
        self.amenities = Amenities(**data.get("amenities"))
        self.images = Images()._import(data.get("images"))
        self.booking_conditions = data.get("booking_conditions")

        return self

    def _export_dict(self) -> dict:
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "location": self.location._export_dict(),
            "description": self.description,
            "amenities": self.amenities._export_dict(),
            "images": self.images._export_dict(),
            "booking_conditions": self.booking_conditions
        }
    
    def to_dict(self) -> dict:
        return self._export_dict()

import json    

if __name__ == "__main__":
    hotel_data = {
        "id": "123",
        "destination_id": 456,
        "name": "Hotel A",
        "location": {
            "lat": 40.7128,
            "lng": -74.0060,
            "address": "123 Main St",
            "city": "New York",
            "country": "USA"
        },
        "description": "A lovely hotel in the heart of New York City",
        "amenities": {
            "general": ["wifi", "breakfast"],
            "room": ["tv", "minibar"]
        },
        "images": {
            "rooms": [{"link": "room1.jpg", "description": "Room 1"}],
            "site": [{"link": "site1.jpg", "description": "Site 1"}],
            "amenities": [{"link": "pool.jpg", "description": "Pool"}]
        },
        "booking_conditions": ["non-refundable", "free cancellation"]
    }

    hotel = Hotel()
    hotel._import(hotel_data)
    print(json.dumps(hotel._export_dict(), indent=2))
    # {
    #     "id": "123",
    #     "destination_id": 456,
    #     "name": "Hotel A",
    #     "location": {
    #         "lat": 40.7128,
    #         "lng": -74.006,
    #         "address": "123 Main St",
    #         "city": "New York",
    #         "country": "USA"
    #     },
    #     "description": "A lovely hotel in the heart of New York City",
    #     "amenities": {
    #         "general": ["wifi", "breakfast"],
    #         "room": ["tv", "minibar"]
    #     },
    #     "images": {
    #         "rooms": [{"link": "room1.jpg", "description": "Room 1"}],
    #         "site": [{"link": "site1.jpg", "description": "Site 1"}],
    #         "amenities": [{"link": "pool.jpg", "description": "Pool"}]
    #     },
    #     "booking_conditions": ["non-refundable", "free cancellation"]
    # }