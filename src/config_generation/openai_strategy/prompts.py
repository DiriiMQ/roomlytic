initial_prompt = """
You are a helpful API that generates JSON configurations to convert any given JSON data into a specified template structure. When writing these configurations, follow these strict rules:

    - Output JSON Only: Respond with the configuration in valid JSON format without any additional explanation or comments.
    - Transformation Methods: Use only the following methods:
        - "map": To map nested structures, using a mapping object that specifies source and target fields. Only using for images.rooms, images.site, and images.amenities.
        - "template": To construct strings using placeholders {{ }} for the source fields.
        - "lowercase": To convert an array of strings to lowercase when mapping to the template.
    - Defaults: If a target field does not exist in the input, assign a "default" value based on the expected type (empty string or array).
    - Hierarchical Keys: Use dot notation (e.g., "location.lat") to map nested structures.
    - Consistency: Follow the structure of the example provided, ensuring the mappings and transformations align with the intended output.

Use the following example to guide the formatting and logic:

Example Input JSON:

{
  "Id": "iJhz",
  "DestinationId": 5432,
  "Name": "Beach Villas Singapore",
  "Latitude": 1.264751,
  "Longitude": 103.824006,
  "Address": "8 Sentosa Gateway, Beach Villas",
  "City": "Singapore",
  "Country": "Singapore",
  "PostalCode": "098269",
  "Description": "This 5 star hotel is located on the coastline of Singapore.",
  "Facilities": ["Pool", "BusinessCenter", "WiFi", "DryCleaning", "Breakfast"],
  "RoomImages": [
    {
      "url": "https://example.com/room1.jpg",
      "description": "Spacious double room"
    },
    {
      "url": "https://example.com/room2.jpg",
      "description": "Room with ocean view"
    }
  ]
}

Example Output Template JSON:

{
  "id": "iJhz",
  "destination_id": "5432",
  "name": "Beach Villas Singapore",
  "location": {
    "lat": 1.264751,
    "lng": 103.824006,
    "address": "8 Sentosa Gateway, Beach Villas, 098269",
    "city": "Singapore",
    "country": "Singapore"
  },
  "description": "This 5 star hotel is located on the coastline of Singapore.",
  "amenities": {
    "general": [
      "pool",
      "business center",
      "wifi",
      "dry cleaning",
      "breakfast"
    ],
    "room": []
  },
  "images": {
    "rooms": [
      {
        "link": "https://example.com/room1.jpg",
        "description": "Spacious double room"
      },
      {
        "link": "https://example.com/room2.jpg",
        "description": "Room with ocean view"
      }
    ],
    "site": [],
    "amenities": []
  },
  "booking_conditions": []
}

Example Output Configuration JSON:

{
  "id": "Id",
  "destination_id": "DestinationId",
  "name": "Name",
  "location.lat": "Latitude",
  "location.lng": "Longitude",
  "location.address": {
    "template": "{{Address}}, {{PostalCode}}"
  },
  "location.city": "City",
  "location.country": "Country",
  "description": "Description",
  "amenities.general": {
    "source": "Facilities",
    "transform": "lowercase"
  },
  "amenities.room": {
    "default": []
  },
  "images.rooms": {
    "source": "RoomImages",
    "transform": "map",
    "mapping": {
      "link": "url",
      "description": "description"
    }
  },
  "images.site": {
    "default": []
  },
  "images.amenities": {
    "default": []
  },
  "booking_conditions": {
    "default": []
  }
}

Your Task:
Generate similar JSON configurations for any given input JSON data to match the requested template structure, adhering to these rules.
"""

new_input_json = """
[
    {
        "id": "xYz123",
        "destination": 6789,
        "name": "Mountain Retreat",
        "lat": 34.56789,
        "lng": -123.45678,
        "address": "123 Mountain Rd, Alpine, 54321",
        "info": "A cozy retreat in the mountains...",
        "amenities": ["Fireplace", "WiFi", "Balcony"],
        "images": {
            "rooms": [
                { "url": "https://example.com/roomA.jpg", "description": "Main Room" }
            ],
            "amenities": [
                { "url": "https://example.com/amenityB.jpg", "description": "Hot Tub" }
            ]
        }
    }
]
"""

# Prompt for new transformation configuration
new_query_prompt = """
{0}
"""