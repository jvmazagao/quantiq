from fastapi import HTTPException
from quantiq.modules.stocks.repositories.stock_repository import StockRepository

class GetStock: 
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def execute(self, ticker: str):
        stock = self.stock_repository.fetch(ticker)
        if not stock:
            raise HTTPException(status_code=404, detail={
                "error": "stock.not.found",
                "ticker": ticker,
                "code": "ST_001"
            })
            
        return stock