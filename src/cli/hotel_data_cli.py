from src.aggregator.hotel_data_aggregator import HotelDataAggregator
from src.cleaner.hotel_data_cleaner import HotelDataCleaner
from src.formatter.hotel_data_formatter import HotelDataFormatter
from src.models.hotel_data_model import Hotel

import json

class HotelDataCLI:
    def __init__(self):
        self.aggregator = HotelDataAggregator()
        self.cleaner = HotelDataCleaner()
        self.formatter = HotelDataFormatter()

        self.suppliers = []

    def get_hotels(self, hotel_ids: list[str], destination_ids: list[str]) -> list[Hotel]:
        formatted_data = self.formatter.filter_and_format(self.suppliers, hotel_ids, destination_ids)
        return formatted_data
    
    def convert_list_hotel_2_list_dict(self, hotels: list[Hotel]) -> list[dict]:
        return [hotel._export_dict() for hotel in hotels]

    def run(self, hotel_ids: list[str], destination_ids: list[str]) -> list[Hotel]:
        self.suppliers = self.aggregator.aggregate_data()
        # cleaned_data = [self.cleaner.clean(hotel) for hotel in suppliers]
        
        # print(json.dumps(formatted_data, indent=2))

        # for supplier in self.suppliers:
        #     print(json.dumps(supplier._export_dict(), indent=2))

        uniq_hotels = self.get_hotels(hotel_ids, destination_ids)

        # print(f"Total suppliers: {len(self.suppliers)}")
        # print(f"Total unique hotels: {len(uniq_hotels)}")

        return uniq_hotels

        # for supplier in self.suppliers:
        #     print(json.dumps(supplier._export_dict(), indent=2))
