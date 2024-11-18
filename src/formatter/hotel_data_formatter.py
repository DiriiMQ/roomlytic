from src.models.supplier_model import Supplier
from src.models.hotel_data_model import Hotel
from src.formatter.merge_strategies.hotel_merger import HotelMerger

class HotelDataFormatter:
    def merge(self, dup_hotels: list[list[Hotel]], strategy_type: str = "default") -> list[Hotel]:
        # Logic to merge data
        hotel_merger = HotelMerger.get_strategy(strategy_type)
        return [hotel_merger.merge(dup_hotels) for dup_hotels in dup_hotels]

    def filter_by_ids(self, hotel_data: list[Supplier], hotel_ids: list[str], destination_ids: list[str]) -> list[Hotel]:
        # Logic to filter data
        hotel_ids_filter = {}
        
        for supplier in hotel_data:
            # print(f"Supplier: {supplier.name}")
            # print(f"Total hotels: {len(supplier.hotels)}")
            for hotel in supplier.hotels:
                if hotel.id in hotel_ids and hotel.destination_id in destination_ids:
                    if hotel.id not in hotel_ids_filter:
                        hotel_ids_filter[hotel.id] = [hotel]
                    else:
                        hotel_ids_filter[hotel.id].append(hotel)

        # print(f"Total unique hotelszz: {len(hotel_ids_filter)}")

        return self.merge(list(hotel_ids_filter.values()))


    def filter_and_format(self, hotel_data: list[Supplier], hotel_ids: list[str], destination_ids: list[str]) -> list[Hotel]:
        # Logic to filter
        unique_hotels = self.filter_by_ids(hotel_data, hotel_ids, destination_ids)

        # Maybe some formatting logic here

        return unique_hotels
