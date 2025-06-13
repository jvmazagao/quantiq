import logging
from quantiq.database.database import transaction
from quantiq.modules.variations.domains.entities import Variations, Variation

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
    
    def fetch(self, stock_id: int) -> Variations | None:
        with transaction() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT stock_id, period, value FROM variations WHERE stock_id = ?", (stock_id,)).fetchall()
            
            if not len(rows):
                return None

            return Variations([Variation(row[0], row[1], row[2]) for row in rows])