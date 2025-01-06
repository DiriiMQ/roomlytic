from .generation_strategy import GenerationStrategy
from .openai_strategy.prompts import initial_prompt, new_input_json, new_query_prompt
from .APIFetcher import APIFetcher

from openai import OpenAI
import json, os, requests

class OpenAIGenerationStrategy(GenerationStrategy, APIFetcher):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # self.initial_teaching()
        pass

    def send_api(self, prompt: str, role: str="user") -> str:
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                        "type": "text",
                        "text": "You are a helpful API that generates JSON configurations to convert any given JSON data into a specified template structure. When writing these configurations, follow these strict rules:\n\n    - Output JSON Only: Respond with the configuration in valid JSON format without any additional explanation or comments.\n    - Transformation Methods: Use only the following methods:\n        - \"map\": To map nested structures, using a mapping object that specifies source and target fields. Only using for images.rooms, images.site, and images.amenities.\n        - \"template\": To construct strings using placeholders {} for the source fields.\n        - \"lowercase\": To convert an array of strings to lowercase when mapping to the template.\n    - Defaults: If a target field does not exist in the input, assign a \"default\" value based on the expected type (empty string or array).\n    - Hierarchical Keys: Use dot notation (e.g., \"location.lat\") to map nested structures.\n    - Consistency: Follow the structure of the example provided, ensuring the mappings and transformations align with the intended output.\n\nUse the following example to guide the formatting and logic:\n\nExample Input JSON:\n\n{\n  \"Id\": \"iJhz\",\n  \"DestinationId\": 5432,\n  \"Name\": \"Beach Villas Singapore\",\n  \"Latitude\": 1.264751,\n  \"Longitude\": 103.824006,\n  \"Address\": \"8 Sentosa Gateway, Beach Villas\",\n  \"City\": \"Singapore\",\n  \"Country\": \"Singapore\",\n  \"PostalCode\": \"098269\",\n  \"Description\": \"This 5 star hotel is located on the coastline of Singapore.\",\n  \"Facilities\": [\"Pool\", \"BusinessCenter\", \"WiFi\", \"DryCleaning\", \"Breakfast\"],\n  \"RoomImages\": [\n    {\n      \"url\": \"https://example.com/room1.jpg\",\n      \"description\": \"Spacious double room\"\n    },\n    {\n      \"url\": \"https://example.com/room2.jpg\",\n      \"description\": \"Room with ocean view\"\n    }\n  ]\n}\n\nExample Output Template JSON:\n\n{\n  \"id\": \"iJhz\",\n  \"destination_id\": \"5432\",\n  \"name\": \"Beach Villas Singapore\",\n  \"location\": {\n    \"lat\": 1.264751,\n    \"lng\": 103.824006,\n    \"address\": \"8 Sentosa Gateway, Beach Villas, 098269\",\n    \"city\": \"Singapore\",\n    \"country\": \"Singapore\"\n  },\n  \"description\": \"This 5 star hotel is located on the coastline of Singapore.\",\n  \"amenities\": {\n    \"general\": [\n      \"pool\",\n      \"business center\",\n      \"wifi\",\n      \"dry cleaning\",\n      \"breakfast\"\n    ],\n    \"room\": []\n  },\n  \"images\": {\n    \"rooms\": [\n      {\n        \"link\": \"https://example.com/room1.jpg\",\n        \"description\": \"Spacious double room\"\n      },\n      {\n        \"link\": \"https://example.com/room2.jpg\",\n        \"description\": \"Room with ocean view\"\n      }\n    ],\n    \"site\": [],\n    \"amenities\": []\n  },\n  \"booking_conditions\": []\n}\n\nExample Output Configuration JSON:\n\n{\n  \"id\": \"Id\",\n  \"destination_id\": \"DestinationId\",\n  \"name\": \"Name\",\n  \"location.lat\": \"Latitude\",\n  \"location.lng\": \"Longitude\",\n  \"location.address\": {\n    \"template\": \"{Address}, {PostalCode}\"\n  },\n  \"location.city\": \"City\",\n  \"location.country\": \"Country\",\n  \"description\": \"Description\",\n  \"amenities.general\": {\n    \"source\": \"Facilities\",\n    \"transform\": \"lowercase\"\n  },\n  \"amenities.room\": {\n    \"default\": []\n  },\n  \"images.rooms\": {\n    \"source\": \"RoomImages\",\n    \"transform\": \"map\",\n    \"mapping\": {\n      \"link\": \"url\",\n      \"description\": \"description\"\n    }\n  },\n  \"images.site\": {\n    \"default\": []\n  },\n  \"images.amenities\": {\n    \"default\": []\n  },\n  \"booking_conditions\": {\n    \"default\": []\n  }\n}\n\nYour Task:\nGenerate similar JSON configurations for any given input JSON data to match the requested template structure, adhering to these rules."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "[\n {\n\"Id\": \"iJhz\",\n\"DestinationId\": 5432,\n\"Name\": \"Beach Villas Singapore\",\n\"Latitude\": 1.264751,\n\"Longitude\": 103.824006,\n\"Address\": \" 8 Sentosa Gateway, Beach Villas \",\n\"City\": \"Singapore\",\n\"Country\": \"SG\",\n\"PostalCode\": \"098269\",\n\"Description\": \" This 5 star hotel is located on the coastline of Singapore.\",\n\"Facilities\": [\n\"Pool\",\n\"BusinessCenter\",\n\"WiFi \",\n\"DryCleaning\",\n\" Breakfast\"\n]\n}\n]"
                        }
                    ]
                    },
                    {
                    "role": "assistant",
                    "content": [
                        {
                        "type": "text",
                        "text": "{\n  \"id\": \"Id\",\n  \"destination_id\": \"DestinationId\",\n  \"name\": \"Name\",\n  \"location.lat\": \"Latitude\",\n  \"location.lng\": \"Longitude\",\n  \"location.address\": {\n    \"template\": \"{Address}, {PostalCode}\"\n  },\n  \"location.city\": \"City\",\n  \"location.country\": {\n    \"template\": \"{Country}\"\n  },\n  \"description\": \"Description\",\n  \"amenities.general\": {\n    \"source\": \"Facilities\",\n    \"transform\": \"lowercase\"\n  },\n  \"amenities.room\": {\n    \"default\": []\n  },\n  \"images.rooms\": {\n    \"default\": []\n  },\n  \"images.site\": {\n    \"default\": []\n  },\n  \"images.amenities\": {\n    \"default\": []\n  },\n  \"booking_conditions\": {\n    \"default\": []\n  }\n}"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {   
                            "type": "text",
                            "text": f"{prompt}"
                        }
                    ],
                }
            ],
            model="gpt-4o-mini",
            response_format={
                "type": "json_object"
            },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content.strip()

    def initial_teaching(self):
        # Send the teaching prompt to OpenAI
        response = self.send_api(initial_prompt, role="system")
        return response
        # pass
    
    def generate_config(self, supplier_info: dict) -> dict:
        global new_query_prompt

        # Add more logics later
        data = self.fetch_api(supplier_info["url"])
        # print(type(data))

        sample = self.get_complete_sample(data)

        new_input_json = json.dumps(sample, indent=4)
        new_query_prompt = new_query_prompt.format(new_input_json)

        # print(new_query_prompt)

        # Send the new query prompt to OpenAI
        response = self.send_api(new_query_prompt)
        # print(response)
        config_json = response
        config_json = json.loads(config_json)

        return config_json


if __name__ == "__main__":
    strategy = OpenAIGenerationStrategy("hidden")
    supplier_info = {
        "name": "Supplier 1",
        "url": "../../sample/sample2.json"
    }
    config = strategy.generate_config(supplier_info)
    print(json.dumps(config, indent=4))