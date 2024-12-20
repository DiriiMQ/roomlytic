from src.aggregator.hotel_data_aggregator import HotelDataAggregator
from src.cleaner.hotel_data_cleaner import HotelDataCleaner
from src.formatter.hotel_data_formatter import HotelDataFormatter
from src.models.hotel_data_model import Hotel
from src.utils.helper_functions import save_to_file

import json, time

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
        self.suppliers = self.cleaner.clean_all_suppliers(self.suppliers)

        save_to_file(
            [supplier._export_dict() for supplier in self.suppliers], 
            f'output/suppliers_{time.strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        # print(json.dumps(self.suppliers, indent=2))

        # for supplier in self.suppliers:
        #     print(json.dumps(supplier._export_dict(), indent=2))

        uniq_hotels = self.get_hotels(hotel_ids, destination_ids)

        # print(f"Total suppliers: {len(self.suppliers)}")
        # print(f"Total unique hotels: {len(uniq_hotels)}")

        return uniq_hotels

        # for supplier in self.suppliers:
        #     print(json.dumps(supplier._export_dict(), indent=2))
