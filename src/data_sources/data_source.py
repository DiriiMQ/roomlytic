import json
import requests

class DataSource:
    def __init__(self, config_file="../configs/suppliers.config.json"):
        with open(config_file) as f:
            self.config = json.load(f)

        print(self.config)

    def fetch_data(self, supplier_name: str) -> list:
        supplier_config = self.config.get(supplier_name)
        if not supplier_config:
            raise ValueError(f"Supplier {supplier_name} is not defined in configuration.")

        url = supplier_config['url']
        field_mappings = supplier_config.get('field_mappings', {})
        transform_function = supplier_config.get('transform_function')

        # Fetch data from supplier
        response = requests.get(url)
        data = response.json()

        # Apply field mappings and transformations
        standardized_data = self._apply_mappings(data, field_mappings)
        if transform_function:
            standardized_data = getattr(self, transform_function)(standardized_data)

        return standardized_data

    def _apply_mappings(self, data: list, mappings: dict) -> list:
        return [
            {mappings.get(key, key): value for key, value in item.items()} for item in data
        ]

    def standard_transform(self, data: list) -> list:
        # Example transform function; add more as needed
        return data

if __name__ == "__main__":
    ds = DataSource()
    