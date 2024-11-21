from generation_strategy import GenerationStrategy

import json, requests

def jaro_distance(s1, s2):
    # Step 1: Calculate matching characters
    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return 0.0
    match_window = max(len1, len2) // 2 - 1

    # Create a boolean array to mark matched characters
    matched1 = [False] * len1
    matched2 = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - match_window)
        end = min(len2, i + match_window + 1)
        for j in range(start, end):
            if s1[i] == s2[j] and not matched2[j]:
                matched1[i] = True
                matched2[j] = True
                matches += 1
                break

    # If no matches, return 0
    if matches == 0:
        return 0.0

    # Step 2: Calculate transpositions
    t = 0
    k = 0
    for i in range(len1):
        if matched1[i]:
            while not matched2[k]:
                k += 1
            if s1[i] != s2[k]:
                t += 1
            k += 1
    t /= 2

    # Step 3: Calculate Jaro distance
    jaro_dist = (matches / len1 + matches / len2 + (matches - t) / matches) / 3
    return jaro_dist

def jaro_winkler_distance(s1, s2, p=0.1, l=4):
    # Step 1: Calculate Jaro distance
    jaro_dist = jaro_distance(s1, s2)
    
    # Step 2: Apply the Winkler adjustment
    # Count common prefix (max 4 characters)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), l)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    # Adjust the Jaro distance with the Winkler correction
    jaro_winkler_dist = jaro_dist + (p * prefix_len * (1 - jaro_dist))
    
    return jaro_winkler_dist


class DefaultGenerationStrategy(GenerationStrategy):
    DEFAULT_STR = {
        "default": ""
    }

    def fetch_api(self, url: str) -> dict:
        """ Fetch data from the API """
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Error fetching data from API: {e}")
            return {}
        
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
    
    def mapping(self, config: dict, sample_keys: list[str]) -> dict:
        # Mapping the sample data to the config
        
        for target_field, source_field in config["config"].items():
            for key in sample_keys:
                if isinstance(source_field, str):
                    keys = key.split(".")
                    scores = [jaro_winkler_distance(target_field, k) for k in keys]
                    if max(scores) > 0.5:
                        config["config"][target_field] = key
                        sample_keys.remove(key)
                        break
                    config["config"][target_field] = self.DEFAULT_STR
                else:
                    pass

        return config
                
        

    def generate_config(self, supplier_info: dict) -> list[dict]:
        """ Generate a configuration based on the supplier information (name and url) """
        config = {
            "name": supplier_info["name"],
            "url": supplier_info["url"],
            "config": {
                "id": "",
                "destination_id": "",
                "name": "",
                "location.lat": "",
                "location.lng": "",
                "location.address": "",
                "location.city": "",
                "location.country": "",
                "description": "",
                "amenities.general": {
                    "default": []
                },
                "amenities.room": {
                    "default": []
                },
                "images.rooms": {
                    "default": []
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
        }

        # Add more logics later
        data = self.fetch_api(supplier_info["url"])
        # print(type(data))

        sample = self.get_complete_sample(data)
        # print(json.dumps(sample, indent=4))
        sample_values = [self.get_nested_value(sample, key) for key in self.get_keys(sample)]
        # print(sample_values)
        sample_keys = [key if isinstance(self.get_nested_value(sample, key), str) else None for key in self.get_keys(sample)]
        # print(sample_keys)
        # Remove None in sample_keys
        sample_keys = list(filter(None, sample_keys))
        print(sample_keys)

        config = self.mapping(config, sample_keys)

        return config
    

if __name__ == "__main__":
    strategy = DefaultGenerationStrategy()
    supplier_info = {
        "name": "Supplier 1",
        "url": "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia"
    }
    config = strategy.generate_config(supplier_info)
    print(json.dumps(config, indent=4))