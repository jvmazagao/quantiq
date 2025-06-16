from typing import Any

from quantiq.modules.stocks.services.stock_services import StockServices


class GetStock:
    def __init__(self, stock_services: StockServices) -> None:
        self.stock_services = stock_services

    def execute(self, ticker: str) -> dict[str, Any]:
        return self.stock_services.get_stock(ticker)
