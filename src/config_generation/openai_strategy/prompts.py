initial_prompt = """
You will transform an input JSON into a fixed goal JSON using specific transformation rules. The goal JSON structure is always the same, but the input JSON can vary. Your task is to generate a configuration JSON that defines how to map and transform fields from the input JSON to the goal JSON.

### Fixed Goal JSON:
[
    {
        "id": "string",
        "destination_id": "integer",
        "name": "string",
        "location": {
            "lat": "float",
            "lng": "float",
            "address": "string",
            "city": "string",
            "country": "string"
        },
        "description": "string",
        "amenities": {
            "general": ["array of strings"],
            "room": ["array of strings"]
        },
        "images": {
            "rooms": [
                { "link": "string", "description": "string" }
            ],
            "site": [
                { "link": "string", "description": "string" }
            ],
            "amenities": [
                { "link": "string", "description": "string" }
            ]
        },
        "booking_conditions": ["array of strings"]
    }
]

### Transformation Rules:
1. **Direct Mapping**: Directly map a field from the input JSON to the goal JSON.
2. **Nested Mapping**: Map fields to nested fields in the goal JSON.
3. **Default Values**: Assign default values to fields not present in the input JSON.
4. **List Transformation**: Transform lists (e.g., lowercase, capitalize).
5. **Mapping Transformation**: Map lists of objects, renaming fields as necessary.
6. **Template Description**: Use templates to construct strings by combining multiple fields.

### Example Input JSON:
[
    {
        "id": "iJhz",
        "destination": 5432,
        "name": "Beach Villas Singapore",
        "lat": 1.264751,
        "lng": 103.824006,
        "address": "8 Sentosa Gateway, Beach Villas, 098269",
        "info": "Located at the western tip of Resorts World Sentosa...",
        "amenities": ["Aircon", "Tv", "Coffee machine", "Kettle"],
        "images": {
            "rooms": [
                { "url": "https://example.com/room1.jpg", "description": "Room 1" }
            ],
            "amenities": [
                { "url": "https://example.com/amenity1.jpg", "description": "Amenity 1" }
            ]
        }
    }
]

### Example Configuration JSON:
{
    "id": "id",
    "destination_id": "destination",
    "name": "name",
    "location.lat": "lat",
    "location.lng": "lng",
    "location.address": "address",
    "location.city": { "default": "Singapore" },
    "location.country": { "default": "Singapore" },
    "description": { "template": "{name} is located in {location[city]}, {location[country]}" },
    "amenities.general": { "default": [] },
    "amenities.room": { "source": "amenities", "transform": "lowercase" },
    "images.rooms": {
        "source": "images.rooms",
        "transform": "map",
        "mapping": { "link": "url", "description": "description" }
    },
    "images.site": { "default": [] },
    "images.amenities": {
        "source": "images.amenities",
        "transform": "map",
        "mapping": { "link": "url", "description": "description" }
    },
    "booking_conditions": { "default": [] }
}

From now on, given a new input JSON, generate only the configuration JSON required to transform the input into the fixed goal JSON using the rules described above.
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
Generate the configuration JSON to transform the following input JSON into the fixed goal JSON:

Input JSON:
{0}
"""