from quantiq.database.database import transaction
import logging
from quantiq.modules.market_values.domains.entities import MarketValues

class MarketValue:
    def __init__(self, stock_id: int, identifier: str, value: str):
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value
    
class MarketValues:
    def __init__(self, values: list[MarketValue]):
        self.values = values
    
    @staticmethod
    def parse(data: dict, stock_id: int):
        return MarketValues([MarketValue(stock_id, identifier, value) for identifier, value in data.items()])

class MarketValuesRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, market_values: MarketValues):
        with transaction() as conn:
            try:
                values = [(value.stock_id, value.identifier, value.value) for value in market_values.values]
                cursor = conn.cursor()
                cursor.executemany("""
                    INSERT INTO market_values (stock_id, identifier, value)
                    VALUES (?, ?, ?)
                    ON CONFLICT (stock_id, identifier) DO UPDATE SET value = excluded.value
                """, values)
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                self.logger.error(f"Error storing market values: {e}")
                conn.rollback()
                raise e 