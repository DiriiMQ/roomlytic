from src.formatter.merge_strategies.hotel_merge_strategy import HotelMergeStrategy
from src.models.hotel_data_model import Hotel, Location, Amenities, Images, Image
from src.utils.helper_functions import get_longer_str, filter_more_general_term

from typing import List

class DefaultHotelMergeStrategy(HotelMergeStrategy):
    def merge(self, hotels: List[Hotel]) -> Hotel:
        if not hotels:
            raise ValueError("No hotels to merge.")

        # Start with the first hotel as the base
        merged_hotel = hotels[0]

        for hotel in hotels[1:]:
            # Merge fields with prioritization logic
            merged_hotel.name = get_longer_str(merged_hotel.name, hotel.name)
            merged_hotel.description = get_longer_str(merged_hotel.description, hotel.description)
            merged_hotel.location = self.merge_location(merged_hotel.location, hotel.location)
            merged_hotel.amenities = self.merge_amenities(merged_hotel.amenities, hotel.amenities)
            merged_hotel.images = self.merge_images(merged_hotel.images, hotel.images)
            merged_hotel.booking_conditions = list(set(merged_hotel.booking_conditions + hotel.booking_conditions))

        return merged_hotel

    def merge_location(self, loc1: Location, loc2: Location) -> Location:
        # Prefer non-null fields in loc2
        return Location(
            lat=loc2.lat or loc1.lat,
            lng=loc2.lng or loc1.lng,
            address=get_longer_str(loc1.address, loc2.address),
            city=get_longer_str(loc1.city, loc2.city),
            country=get_longer_str(loc1.country, loc2.country),
        )

    def merge_amenities(self, am1: Amenities, am2: Amenities) -> Amenities:
        # Prefer specific fields over general ones
        am =  Amenities(
            general=list(set(am1.general + am2.general)),
            room=list(set(am1.room + am2.room)),
        )

        # Filter spaced amenities like "bath tub" and "bathtub"
        am.general = [a for a in am.general if a.replace(" ", "") not in am.room]
        am.room = [a for a in am.room if a.replace(" ", "") not in am.general]

        # Filter sub amenities like "pool" and "indoor pool" -> keep the shorter one as it's more general
        am.general = filter_more_general_term(am.general)
        am.room = filter_more_general_term(am.room)

        # Remove duplicated amenities in room from general
        am.general = [a for a in am.general if a.replace(" ", "") not in am.room]

        return am

    def merge_images(self, img1: Images, img2: Images) -> Images:
        # Combine images and remove duplicates by link
        return Images(
            rooms=self.merge_image_lists(img1.rooms, img2.rooms),
            site=self.merge_image_lists(img1.site, img2.site),
            amenities=self.merge_image_lists(img1.amenities, img2.amenities),
        )

    def merge_image_lists(self, list1: List[Image], list2: List[Image]) -> List[Image]:
        seen = set()
        merged_list = []
        for image in list1 + list2:
            if image.link not in seen:
                merged_list.append(image)
                seen.add(image.link)
        return merged_list
