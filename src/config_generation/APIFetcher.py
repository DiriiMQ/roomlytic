import requests

class APIFetcher:
    def __init__(self):
        pass

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