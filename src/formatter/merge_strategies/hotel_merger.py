from src.formatter.merge_strategies.hotel_merge_strategy import HotelMergeStrategy
from src.formatter.merge_strategies.default_hotel_merge_strategy import DefaultHotelMergeStrategy

class HotelMerger:
    HOTEL_MERGE_STRATEGIES = {
        "default": DefaultHotelMergeStrategy,
    }

    @staticmethod
    def get_strategy(strategy_type: str) -> HotelMergeStrategy:
        if strategy_type in HotelMerger.HOTEL_MERGE_STRATEGIES:
            return HotelMerger.HOTEL_MERGE_STRATEGIES[strategy_type]()
        
        raise ValueError(f"Unknown strategy type: {strategy_type}")
