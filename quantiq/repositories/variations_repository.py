import logging

from quantiq.database.database import transaction

class Variation:
    def __init__(self, stock_id: int, period: str | int, value: float):
        self.stock_id = stock_id
        self.period = period
        self.value = value


class Variations:
    def __init__(self, variations: list[Variation]):
        self.variations = variations

    @staticmethod
    def parse(data: dict, stock_id: int):
        return Variations([Variation(stock_id, period, value) for period, value in data.items()])

class VariationsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, data: dict, stock_id: int):
        with transaction() as conn:
            try:
                variations = Variations.parse(data, stock_id)
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
