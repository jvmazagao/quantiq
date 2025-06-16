import logging

from quantiq.database.database import transaction
from quantiq.modules.financial_results.domains.entities import (
    FinancialResult,
    FinancialResults,
)


class FinancialResultsRepository:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def store(self, financial_results: FinancialResults) -> int:
        with transaction() as conn:
            try:
                values = [
                    (
                        financial_result.stock_id,
                        financial_result.period,
                        financial_result.identifier,
                        financial_result.value,
                    )
                    for financial_result in financial_results.financial_results
                ]
                cursor = conn.cursor()
                query = """
                INSERT INTO financial_period (stock_id, period, identifier, value)
                VALUES (?, ?, ?, ?)
                ON CONFLICT (stock_id, period, identifier) DO UPDATE SET value = excluded.value
                """
                cursor.executemany(query, values)
                conn.commit()
                return cursor.lastrowid  # type: ignore
            except Exception as e:
                self.logger.error(f"Error storing financial results: {e}")
                conn.rollback()
                raise e

    def fetch(self, stock_id: int) -> FinancialResults | None:
        with transaction() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT id, period, identifier, value FROM financial_period WHERE stock_id = ?",
                (stock_id,),
            ).fetchall()

            if not len(rows):
                return None

            return FinancialResults(
                [FinancialResult(row[0], row[1], row[2], row[3]) for row in rows]
            )
