from fastapi import APIRouter

from quantiq.modules.stocks.use_cases.insert_stock import InsertStock
from quantiq.modules.stocks.use_cases.get_stock import GetStock

class StockRouter(APIRouter):
    def __init__(self, insert_stock: InsertStock, get_stock: GetStock):
        super().__init__(
            tags=["stocks"]
        )
        self.insert_stock_use_case = insert_stock
        self.get_stock_use_case = get_stock
        self.register_routes()

    def register_routes(self):
        self.add_api_route("/{type}/{ticker}", self.insert_stock_use_case.execute, methods=["POST"])
        self.add_api_route("/stocks/{ticker}", self.get_stock_use_case.execute, methods=["GET"])
    
        
