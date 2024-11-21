from .generation_strategy import GenerationStrategy
from .openai_strategy.prompts import initial_prompt, new_input_json, new_query_prompt
from .APIFetcher import APIFetcher

from openai import OpenAI
import json, os, requests

class OpenAIGenerationStrategy(GenerationStrategy, APIFetcher):
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
        # pass
    
    def generate_config(self, supplier_info: dict) -> dict:
        global new_query_prompt

        # Add more logics later
        data = self.fetch_api(supplier_info["url"])
        # print(type(data))

        sample = self.get_complete_sample(data)

        new_input_json = json.dumps(sample, indent=4)
        new_query_prompt = new_query_prompt.format(new_input_json)

        print(new_query_prompt)

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