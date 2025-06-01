from quantiq.modules.balance_sheet.repositories.balance_sheets_repository import BalanceSheetsRepository
from quantiq.modules.balance_sheet.domains.entities import BalanceSheets

class BalanceSheetService:
    def __init__(self, balance_sheets_repository: BalanceSheetsRepository):
        self.balance_sheets_repository = balance_sheets_repository

    def store(self, balance_sheets: dict, stock_id: int):
        balance_sheets = BalanceSheets.parse(balance_sheets, stock_id)
        stored_balance_sheets = self.balance_sheets_repository.store(balance_sheets)
        return stored_balance_sheets