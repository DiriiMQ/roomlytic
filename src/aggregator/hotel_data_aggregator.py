from src.data_sources.data_source import DataSource
from src.data_sources.transformation import Transformation

import json

class HotelDataAggregator:
    def __init__(self, config_file="src/configs/suppliers.config.json"):
        with open(config_file) as f:
            self.config = json.load(f)

        self.data_source = DataSource()
        self.transformer = Transformation()

        self.suppliers = self.get_all_suppliers()

        print(self.suppliers)

    def get_all_suppliers(self) -> list[str]:
        return [supplier["name"] for supplier in self.config["suppliers"]]

    def aggregate_data(self) -> list:
        all_data = []
        for supplier in self.suppliers:
            transformed_data = self.data_source.fetch_data(supplier, transformer=self.transformer)
            all_data.extend([{supplier: transformed_data}])
        return self.merge_data(all_data)

    def merge_data(self, data: list) -> list:
        # Logic to merge data by hotel ID, selecting the best data from each supplier
        return data
