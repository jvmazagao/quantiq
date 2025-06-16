from quantiq.modules.balance_sheet.domains.entities import BalanceSheet, BalanceSheets
from quantiq.modules.balance_sheet.repositories.balance_sheets_repository import (
    BalanceSheetsRepository,
)


class BalanceSheetService:
    def __init__(self, balance_sheets_repository: BalanceSheetsRepository):
        self.balance_sheets_repository = balance_sheets_repository

    def store(self, balance_sheets: dict[str, str], stock_id: int) -> BalanceSheets:
        sheets = BalanceSheets.parse(balance_sheets, stock_id)
        self.balance_sheets_repository.store(sheets)
        return sheets

    def fetch(self, stock_id: int) -> list[BalanceSheet]:
        sheet = self.balance_sheets_repository.fetch(stock_id)

        if not sheet:
            return []

        return sheet
