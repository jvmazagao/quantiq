from quantiq.modules.balance_sheet.repositories.balance_sheets_repository import BalanceSheetsRepository
from quantiq.modules.balance_sheet.services.service import BalanceSheetService

__all__ = ["make_balance_sheet_service"]

def make_balance_sheet_repository():
    return BalanceSheetsRepository()

def make_balance_sheet_service():
    return BalanceSheetService(make_balance_sheet_repository())