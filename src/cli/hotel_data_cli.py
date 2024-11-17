from src.aggregator.hotel_data_aggregator import HotelDataAggregator
from src.cleaner.hotel_data_cleaner import HotelDataCleaner
from src.formatter.hotel_data_formatter import HotelDataFormatter

import json

class HotelDataCLI:
    def __init__(self):
        self.aggregator = HotelDataAggregator([AcmeDataSource(), PatagoniaDataSource(), PaperfliesDataSource()])
        self.cleaner = HotelDataCleaner()
        self.formatter = HotelDataFormatter()

    def run(self, hotel_ids: str, destination_ids: str):
        data = self.aggregator.aggregate_data()
        cleaned_data = [self.cleaner.clean(hotel) for hotel in data]
        formatted_data = self.formatter.filter_and_format(cleaned_data, hotel_ids, destination_ids)
        print(json.dumps(formatted_data, indent=2))
