import logging
from typing import List

from quantiq.modules.balance_sheet.domains.entities import BalanceSheet
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
            
    def fetch(self, stock_id: int) -> List[BalanceSheet]:
        with transaction() as conn:
            try:
                cursor = conn.cursor()
                query = """
                SELECT stock_id, identifier, value FROM balance_sheet WHERE stock_id = ?
                """
                cursor.execute(query, (stock_id,))
                return [BalanceSheet(
                    stock_id=row[0],
                    identifier=row[1],
                    value=row[2]
                ) for row in cursor.fetchall()]
            except Exception as e:
                self.logger.error(f"Error fetching balance sheets: {e}")
                conn.rollback()
                raise e