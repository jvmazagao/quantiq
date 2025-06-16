class MarketValue:
    def __init__(self, stock_id: int, identifier: str, value: str) -> None:
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value


class MarketValues:
    def __init__(self, values: list[MarketValue]) -> None:
        self.values = values

    @staticmethod
    def parse(data: dict[str, str], stock_id: int) -> "MarketValues":
        return MarketValues(
            [
                MarketValue(stock_id, identifier, value)
                for identifier, value in data.items()
            ]
        )
