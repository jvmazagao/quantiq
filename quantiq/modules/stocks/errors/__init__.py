from quantiq.core.errors import NotFoundException

__all__ = ["StockNotFoundException"]

class StockNotFoundException(NotFoundException):
    def __init__(self, ticker: str):
        super().__init__(detail={
            "error": "stock.not.found",
            "ticker": ticker,
            "code": "ST_001"
        })