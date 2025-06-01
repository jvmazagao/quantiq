class MarketValue:
    def __init__(self, stock_id: int, identifier: str, value: str):
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value
    
class MarketValues:
    def __init__(self, values: list[MarketValue]):
        self.values = values
    
    @staticmethod
    def parse(data: dict, stock_id: int):
        return MarketValues([MarketValue(stock_id, identifier, value) for identifier, value in data.items()]) 