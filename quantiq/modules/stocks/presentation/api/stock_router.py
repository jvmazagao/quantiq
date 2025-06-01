from fastapi import APIRouter

from quantiq.modules.stocks.use_cases.insert_stock import InsertStock

class StockRouter(APIRouter):
    def __init__(self, insert_stock: InsertStock):
        super().__init__(
            tags=["stocks"]
        )
        self.insert_stock_use_case = insert_stock
        self.register_routes()

    def register_routes(self):
        self.add_api_route("/stocks/{ticker}", self.insert_stock_use_case.execute, methods=["POST"])
    
        
