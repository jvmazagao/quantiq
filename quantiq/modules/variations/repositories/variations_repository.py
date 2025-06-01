import logging
from quantiq.database.database import transaction
from quantiq.modules.variations.domains.entities import Variations

class VariationsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, variations: Variations):
        with transaction() as conn:
            try:
                values = [(variation.stock_id, variation.period, variation.value) for variation in variations.variations]
                cursor = conn.cursor()
                query = """
                    INSERT INTO variations (stock_id, period, value)
                    VALUES (?, ?, ?)
                    ON CONFLICT (stock_id, period) DO UPDATE SET value = excluded.value
                """
                cursor.executemany(query, values)
                conn.commit()
            except Exception as e:
                self.logger.error(f"Error storing variation: {e}")
                conn.rollback() 