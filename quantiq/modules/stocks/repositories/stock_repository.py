import sqlite3

import logging

from quantiq.database.database import transaction
from quantiq.modules.stocks.domain.entities import Stock

class StockRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, stock: Stock):
        with transaction() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stocks (ticker, type, name, sector, subsector)
                    VALUES (?, ?, ?, ?, ?)
                """, (stock.ticker, stock.type, stock.name, stock.sector, stock.subsector))
                conn.commit()
                self.logger.info(f"Stock {stock.ticker} inserted successfully")
                res = self.fetch(stock.ticker)
                return res
            except sqlite3.Error as e:
                if isinstance(e, sqlite3.IntegrityError):
                    self.logger.error(f"Stock {stock.ticker} already exists")
                    return self.fetch(stock.ticker)
                self.logger.error(f"Error inserting stock {stock.ticker}: {e}")
                conn.rollback()
                raise e
    
    def fetch(self, ticker: str):
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, ticker, type, name, sector, subsector FROM stocks WHERE ticker = ?", (ticker.upper(),))
            row = cursor.fetchone()
            if row:
                return Stock(
                    id=row[0],
                    ticker=row[1],
                    type=row[2],
                    name=row[3],
                    sector=row[4],
                    subsector=row[5]
                )
            return None

    def delete(self, ticker: str):
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE ticker = ?", (ticker.upper(),))
            conn.commit()
            self.logger.info(f"Stock {ticker} deleted successfully")