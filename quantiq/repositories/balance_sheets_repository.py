import logging

from quantiq.database.database import transaction

class BalanceSheet:
    def __init__(self, stock_id, identifier, value):
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value

class BalanceSheets:
    def __init__(self, balance_sheets):
        self.balance_sheets = balance_sheets

    @staticmethod
    def parse(data, stock_id):
        balance_sheets = []
        for identifier, value in data.items():
            balance_sheets.append(BalanceSheet(stock_id, identifier, value))
        return BalanceSheets(balance_sheets)

class BalanceSheetsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, balance_sheets, stock_id):
        with transaction() as conn:
            try:
                balance_sheets = BalanceSheets.parse(balance_sheets, stock_id)
                values = []
                for balance_sheet in balance_sheets.balance_sheets:
                    values.append((balance_sheet.stock_id, balance_sheet.identifier, balance_sheet.value))
                cursor = conn.cursor()
                print(values)
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