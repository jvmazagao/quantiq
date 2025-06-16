class Variation:
    def __init__(self, stock_id: int, period: str | int, value: float) -> None:
        self.stock_id = stock_id
        self.period = period
        self.value = value


class Variations:
    def __init__(self, variations: list[Variation]) -> None:
        self.variations = variations

    @staticmethod
    def parse(data: dict[str, float | int], stock_id: int) -> "Variations":
        if not data:
            return Variations([])
        return Variations(
            [
                Variation(stock_id, period, value)
                for period, value in data.items()
                if value is not None
            ]
        )
