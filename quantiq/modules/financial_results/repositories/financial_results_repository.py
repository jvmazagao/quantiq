import logging
from quantiq.database.database import transaction
from quantiq.modules.financial_results.domains.entities import FinancialResults

class FinancialResultsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, financial_results: FinancialResults):
        with transaction() as conn:
            try:
                values = [(
                    financial_result.stock_id,
                    financial_result.period,
                    financial_result.identifier,
                    financial_result.value
                ) for financial_result in financial_results.financial_results]
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