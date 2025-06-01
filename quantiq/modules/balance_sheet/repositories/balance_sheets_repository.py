import logging
from quantiq.core.repositories.repo import Repository
from quantiq.database.database import transaction
from quantiq.modules.balance_sheet.domains.entities import BalanceSheets


class BalanceSheetsRepository(Repository):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, balance_sheets: BalanceSheets):
        with transaction() as conn:
            try:
                values = []
                for balance_sheet in balance_sheets.balance_sheets:
                    values.append((balance_sheet.stock_id, balance_sheet.identifier, balance_sheet.value))
                cursor = conn.cursor()
                query = """
                INSERT INTO balance_sheet (stock_id, identifier, value)
                VALUES (?, ?, ?)
                ON CONFLICT (stock_id, identifier) DO UPDATE SET value = excluded.value
                """
                cursor.executemany(query, values)
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                self.logger.error(f"Error storing balance sheets: {e}")
                conn.rollback()
                raise e