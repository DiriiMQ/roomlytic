class HotelDataAggregator:
    def __init__(self, sources: list[IDataSource]):
        self.sources = sources

    def aggregate_data(self) -> list:
        all_data = []
        for source in self.sources:
            all_data.extend(source.fetch_data())
        return self.merge_data(all_data)
    
    def merge_data(self, data: list) -> list:
        # Logic to merge data by hotel ID, selecting the best data from each supplier
        pass
