from dataclasses import dataclass, field
from typing import List, Optional
from src.models.hotel_data_model import Hotel

@dataclass
class Supplier:
    name: str = ""
    hotels: List[Hotel] = field(default_factory=list)

    def _import(self, data: dict):
        self.name = data.get("name", "")
        self.hotels = [Hotel(**hotel_data) for hotel_data in data.get("hotels", [])]

    def _export_dict(self):
        return {
            "name": self.name,
            "hotels": [hotel.to_dict() for hotel in self.hotels]
        }

# Example usage
if __name__ == "__main__":
    supplier_data = {
        "name": "Sample Supplier",
        "hotels": [
            {
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
        ]
    }

    supplier = Supplier()
    supplier._import(supplier_data)
    print(supplier._export_dict())