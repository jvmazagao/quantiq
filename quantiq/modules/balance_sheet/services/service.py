from typing import List

from quantiq.modules.balance_sheet.repositories.balance_sheets_repository import BalanceSheetsRepository
from quantiq.modules.balance_sheet.domains.entities import BalanceSheets
from quantiq.modules.balance_sheet.domains.entities import BalanceSheet

class BalanceSheetService:
    def __init__(self, balance_sheets_repository: BalanceSheetsRepository):
        self.balance_sheets_repository = balance_sheets_repository

    def store(self, balance_sheets: dict, stock_id: int):
        balance_sheets = BalanceSheets.parse(balance_sheets, stock_id)
        stored_balance_sheets = self.balance_sheets_repository.store(balance_sheets)
        return stored_balance_sheets
    
    def fetch(self, stock_id: int) -> List[BalanceSheet] | None:
        sheet = self.balance_sheets_repository.fetch(stock_id)
        
        if not sheet:
            return None
        
        return sheet