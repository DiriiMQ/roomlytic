from .generation_strategy import GenerationStrategy
from .openai_strategy.prompts import initial_prompt, new_input_json, new_query_prompt

from openai import OpenAI
import json, os, requests

class OpenAIGenerationStrategy(GenerationStrategy):
    def __init__(self, OPENAI_API_KEY):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.initial_teaching()
        pass

    def send_api(self, prompt: str) -> str:
        response = self.client.completions.create(
            prompt=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="gpt-4o-mini",
        )

        return response.choices[0].text.strip()

    def initial_teaching(self):
        # Send the teaching prompt to OpenAI
        response = self.send_api(initial_prompt)
        return response.choices[0].text.strip()

    def fetch_api(self, url: str) -> dict:
        """ Fetch data from the API """
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            raise f"Error fetching data from API: {e}"
    
    def get_keys(self, data: dict, prefix: str = "") -> list[str]:
        keys = []
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                keys.extend(self.get_keys(value, full_key))
            else:
                keys.append(full_key)
        return keys
    
    def get_nested_value(self, data, key_path):
        """Retrieve value from nested dictionary using dot notation."""
        keys = key_path.split(".")
        for key in keys:
            data = data.get(key, {})
        return data

    def set_nested_value(self, data, key_path, value):
        """Set value in nested dictionary using dot notation."""
        keys = key_path.split(".")
        for key in keys[:-1]:
            data = data.setdefault(key, {})
        data[keys[-1]] = value
        
    def get_complete_sample(self, raw_data: list[dict]) -> dict:
        # All elements in the raw_data have the same structure 
        # But some value of fields may be null
        # Replace null fields with an arbitrary value from other elements
        # Deep copy the dict

        sample = {}
        keys = self.get_keys(raw_data[0])
        for key in keys:
            for item in raw_data:
                value = self.get_nested_value(item, key)
                if value is not None:
                    if isinstance(value, int) or isinstance(value, float):
                        self.set_nested_value(sample, key, str(value))
                    else:
                        self.set_nested_value(sample, key, value)
                    break

        return sample
    
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
        config_json = response.choices[0].text.strip()
        config_json = json.loads(config_json)

        return config_json


if __name__ == "__main__":
    strategy = OpenAIGenerationStrategy("abc")
    supplier_info = {
        "name": "Supplier 1",
        "url": "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia"
    }
    config = strategy.generate_config(supplier_info)
    print(json.dumps(config, indent=4))