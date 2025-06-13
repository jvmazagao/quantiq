class Variation:
    def __init__(self, stock_id: int, period: str | int, value: float):
        self.stock_id = stock_id
        self.period = period
        self.value = value


class Variations:
    def __init__(self, variations: list[Variation]):
        self.variations = variations

    @staticmethod
    def parse(data: dict, stock_id: int):
        if not data:
            return Variations([])
        return Variations([Variation(stock_id, period, value) for period, value in data.items() if value is not None]) 