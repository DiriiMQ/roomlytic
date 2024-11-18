from .transform_factory import TransformationFactory
from .transformation_strategies import TemplateTransformation, DefaultTransformation

import json

class Transformation:
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

    def transform_json_with_config(self, source_json, config):
        transformed_data = []
        
        for item in source_json:
            transformed_item = {}

            for target_field, source_field in config["config"].items():
                if isinstance(source_field, str):
                    # Direct mapping
                    value = self.get_nested_value(item, source_field)
                    self.set_nested_value(transformed_item, target_field, value)
                
                elif isinstance(source_field, dict):
                    # Handle templates, defaults, or transformations
                    if "template" in source_field:
                        value = TemplateTransformation().transform(item, source_field)
                    elif "default" in source_field:
                        value = DefaultTransformation().transform(item, source_field)
                    elif "source" in source_field:
                        source_value = self.get_nested_value(item, source_field["source"])
                        
                        transform_type = source_field.get("transform")
                        if transform_type:
                            strategy = TransformationFactory.get_transformation(transform_type)()
                            # print(strategy)
                            value = strategy.transform(source_value, source_field)
                        else:
                            value = source_value

                    self.set_nested_value(transformed_item, target_field, value)
            
            transformed_data.append(transformed_item)
        
        return transformed_data


if __name__ == "__main__":
    # source_json = [
    #     {
    #         "name": "Hotel A",
    #         "location": {
    #             "city": "New York",
    #             "country": "USA"
    #         },
    #         "rooms": [
    #             {"type": "double", "price": 200},
    #             {"type": "single", "price": 150}
    #         ]
    #     },
    #     {
    #         "name": "Hotel B",
    #         "location": {
    #             "city": "San Francisco",
    #             "country": "USA"
    #         },
    #         "rooms": [
    #             {"type": "queen", "price": 250},
    #             {"type": "single", "price": 180}
    #         ]
    #     }
    # ]

    # config = {
    #     "fields": {
    #         "hotel_name": "name",
    #         "loc.city": "location.city",
    #         "loc.country": "location.country",
    #         "room_types": {
    #             "source": "rooms",
    #             "transform": "map",
    #             "mapping": {
    #                 "type": "type",
    #                 "cost": "price"
    #             }
    #         }
    #     }
    # }
    source_json = [
        {
            "name": "Hotel A",
            "location": {
                "city": "New York",
                "country": "USA"
            },
        }
    ]
    config = {
        "config": {
            "hotel_name": "name",
            "city": "location.city",
            "country": "location.country",
            "description": {
                "template": "{name} is located in {location[city]}, {location[country]}"
            },
            "amenities": {
                "default": ["wifi", "pool"]
            },
            "lowercase_example": {
                "source": "name",
                "transform": "lowercase"
            },
            "map_example": {
                "source": "location",
                "transform": "map",
                "mapping": {
                    "city_name": "city",
                    "country_name": "country"
                }
            }
        }
    }

    print("Source JSON:")
    print(json.dumps(source_json, indent=2))

    print("\nTransforming...")

    transformer = Transformation()
    transformed_data = transformer.transform_json_with_config(source_json, config)
    print(json.dumps(transformed_data, indent=2))