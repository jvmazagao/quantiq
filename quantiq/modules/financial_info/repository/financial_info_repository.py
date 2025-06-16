import logging

from quantiq.database.database import transaction
from quantiq.modules.financial_info.domain.entities import FinancialInfo


class FinancialInfoRepository:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def store(self, financial_info: FinancialInfo) -> int:
        with transaction() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO financial_info (stock_id, price, min_52_sem, max_52_sem, last_price_date, volume_by_2m)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT (stock_id) DO UPDATE SET price = excluded.price, min_52_sem = excluded.min_52_sem, max_52_sem = excluded.max_52_sem, last_price_date = excluded.last_price_date, volume_by_2m = excluded.volume_by_2m
                """,
                    (
                        financial_info.stock_id,
                        financial_info.price,
                        financial_info.min_52_sem,
                        financial_info.max_52_sem,
                        financial_info.last_price_date,
                        financial_info.volume_by_2m,
                    ),
                )
                conn.commit()
                return cursor.lastrowid  # type: ignore
            except Exception as e:
                self.logger.error(f"Error storing financial info: {e}")
                conn.rollback()
                raise e

    def fetch(self, stock_id: int) -> FinancialInfo | None:
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT stock_id, price, min_52_sem, max_52_sem, last_price_date, volume_by_2m FROM financial_info WHERE stock_id = ?",
                (stock_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            return FinancialInfo(
                stock_id=row[0],
                price=row[1],
                min_52_sem=row[2] if row[2] is not None else 0.0,
                max_52_sem=row[3] if row[3] is not None else 0.0,
                last_price_date=row[4],
                volume_by_2m=row[5],
            )

    def delete(self, stock_id: int) -> None:
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM financial_info WHERE stock_id = ?", (stock_id,))
            conn.commit()
            self.logger.info(
                f"Financial info for stock {stock_id} deleted successfully"
            )
