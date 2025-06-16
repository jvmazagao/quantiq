from datetime import datetime


class FinancialInfo:
    def __init__(
        self,
        stock_id: int,
        price: float,
        min_52_sem: float,
        max_52_sem: float,
        last_price_date: datetime,
        volume_by_2m: int,
    ):
        self.stock_id = stock_id
        self.price = price
        self.min_52_sem = min_52_sem
        self.max_52_sem = max_52_sem
        self.last_price_date = last_price_date
        self.volume_by_2m = volume_by_2m

    @staticmethod
    def parse(data: dict, stock_id: int) -> "FinancialInfo":
        return FinancialInfo(
            stock_id,
            data["cotacao"],
            data["min_52_sem"],
            data["max_52_sem"],
            data["data_ult_cot"],
            data["vol_med_2m"],
        )
