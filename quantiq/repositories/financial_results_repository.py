import logging
from quantiq.database.database import transaction

class FinancialResult:
    def __init__(self, stock_id: int, period: str, identifier: str, value: str):
        self.stock_id = stock_id
        self.period = period
        self.identifier = identifier
        self.value = value


class FinancialResults:
    def __init__(self, financial_results: list[FinancialResult]):
        self.financial_results = financial_results

    @staticmethod
    def parse(data: dict, stock_id: int):
        financial_results = []
        for period, values in data.items():
            for identifier, value in values.items():
                financial_result = FinancialResult(stock_id, period, identifier, value)
                financial_results.append(financial_result)
        return FinancialResults(financial_results)

class FinancialResultsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, financial_results: dict, stock_id: int):
        with transaction() as conn:
            try:
                financial_results = FinancialResults.parse(financial_results, stock_id)
                values = []
                for financial_result in financial_results.financial_results:
                    values.append((
                        financial_result.stock_id,
                        financial_result.period,
                        financial_result.identifier,
                        financial_result.value
                    ))
                cursor = conn.cursor()
                query = """
                INSERT INTO financial_period (stock_id, period, identifier, value)
                VALUES (?, ?, ?, ?)
                ON CONFLICT (stock_id, period, identifier) DO UPDATE SET value = excluded.value
                """
                cursor.executemany(query, values)
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                self.logger.error(f"Error storing financial results: {e}")
                conn.rollback()
                raise e
                