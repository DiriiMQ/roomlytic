import json
import requests

from src.data_sources.transformation import Transformation
from src.models.hotel_data_model import Hotel

class DataSource:
    def __init__(self, config_file="src/configs/suppliers.config.json"):
        with open(config_file) as f:
            self.config = json.load(f)

        # print(self.config)
        # print("Data source initialized.")

    def fetch_url(self, url):
        # response = requests.get(url)
        # return response.json()

        # url is the path to a json file (temporary)
        with open(url) as f:
            return json.load(f)

    def fetch_data(self, supplier_name: str, transformer: Transformation) -> list:
        supplier_config = next((supplier for supplier in self.config["suppliers"] if supplier["name"] == supplier_name), None)
        if not supplier_config:
            raise ValueError(f"Supplier {supplier_name} is not defined in configuration.")
        
        url = supplier_config['url']
        field_mappings = { 'config': supplier_config.get('config', {}) }
        
        response = self.fetch_url(url)
        data = response
        # print(f"Data: {data}")
        # print(f"Field mappings: {field_mappings}")

        transformed_data = transformer.transform_json_with_config(data, field_mappings)

        hotels = []

        for item in transformed_data:
            hotel = Hotel()
            hotel._import(item)
            hotels.append(hotel)

        # print(f"Transformed data: {transformed_data}")

        return hotels

    def _apply_mappings(self, data: list, mappings: dict) -> list:
        return [
            {mappings.get(key, key): value for key, value in item.items()} for item in data
        ]

    def standard_transform(self, data: list) -> list:
        # Example transform function; add more as needed
        return data

if __name__ == "__main__":
    ds = DataSource()
    transformer = Transformation()
    res = ds.fetch_data("sample/sample2.json", transformer)
    print(json.dumps(res, indent=2))
    
    