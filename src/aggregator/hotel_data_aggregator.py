from src.data_sources.data_source import DataSource
from src.data_sources.transformation import Transformation
from src.models.supplier_model import Supplier

import json

class HotelDataAggregator:
    def __init__(self, config_file="src/configs/suppliers.config.json"):
        self.data_source = DataSource()
        self.transformer = Transformation()

        self.config = {}
        self.suppliers = []
        self.all_data = []

        self.init(config_file=config_file)

        # print(self.suppliers)

    def init(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)
        self.suppliers = self.get_all_suppliers()

    def get_all_suppliers(self) -> list[(str, str)]:
        return [(supplier["name"], supplier["url"]) for supplier in self.config["suppliers"]]

    def aggregate_data(self) -> list[Supplier]:
        self.all_data = []
        for supplier, url in self.suppliers:
            transformed_data = self.data_source.fetch_data(supplier, transformer=self.transformer)
            supplier_data = Supplier(supplier, url, transformed_data)
            self.all_data.append(supplier_data)
        
        return self.merge_data(self.all_data)

    def merge_data(self, data: list) -> list:
        # Logic to merge data by hotel ID, selecting the best data from each supplier
        return data
