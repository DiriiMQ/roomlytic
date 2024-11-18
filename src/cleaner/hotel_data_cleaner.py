from src.models.hotel_data_model import Hotel
from src.models.supplier_model import Supplier
from src.utils.helper_functions import standardize_text_with_textacy

class HotelDataCleaner:
    def standardize_text(self, hotel_data: Hotel) -> Hotel:
        hotel_data.name = standardize_text_with_textacy(hotel_data.name)
        hotel_data.description = standardize_text_with_textacy(hotel_data.description)
        hotel_data.location.address = standardize_text_with_textacy(hotel_data.location.address)
        hotel_data.location.city = standardize_text_with_textacy(hotel_data.location.city)
        hotel_data.location.country = standardize_text_with_textacy(hotel_data.location.country)

        hotel_data.amenities.general = [standardize_text_with_textacy(amenity) for amenity in hotel_data.amenities.general]
        hotel_data.amenities.room = [standardize_text_with_textacy(amenity) for amenity in hotel_data.amenities.room]

        for image in hotel_data.images.rooms + hotel_data.images.site + hotel_data.images.amenities:
            image.description = standardize_text_with_textacy(image.description)
            image.link = standardize_text_with_textacy(image.link)

        return hotel_data

    def clean(self, hotel_data: Hotel) -> Hotel:
        # Logic to clean data

        hotel_data = self.standardize_text(hotel_data)
        
        return hotel_data
    
    def clean_supplier(self, supplier: Supplier) -> Supplier:
        # Logic to clean data
        supplier.hotels = [self.clean(hotel) for hotel in supplier.hotels]
        return supplier
    
    def clean_all_suppliers(self, suppliers: list[Supplier]) -> list[Supplier]:
        # Logic to clean data
        return [self.clean_supplier(supplier) for supplier in suppliers]
