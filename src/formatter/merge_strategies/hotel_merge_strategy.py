from typing import List
from abc import ABC, abstractmethod

from src.models.hotel_data_model import Hotel

class HotelMergeStrategy(ABC):
    @abstractmethod
    def merge(self, hotels: List[Hotel]) -> Hotel:
        pass
