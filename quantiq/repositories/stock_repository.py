import sqlite3

import logging

from quantiq.database.database import transaction

class Stock:
    def __init__(self, ticker: str, type: str, name: str, sector: str, subsector: str, id: int = None):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.name = name
        self.sector = sector
        self.subsector = subsector
    
    @staticmethod
    def parse(data: dict):
        return Stock(
            ticker=data["papel"],
            type=data["tipo"],
            name=data["empresa"],
            sector=data["setor"],
            subsector=data["subsetor"]
        )

class StockRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, stock_data: dict):
        with transaction() as conn:
            try:
                stock = Stock.parse(stock_data)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stocks (ticker, type, name, sector, subsector)
                    VALUES (?, ?, ?, ?, ?)
                """, (stock.ticker, stock.type, stock.name, stock.sector, stock.subsector))
                conn.commit()
                self.logger.info(f"Stock {stock.ticker} inserted successfully")
                return { 'id': cursor.lastrowid, 'ticker': stock.ticker }
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
            cursor.execute("SELECT * FROM stocks WHERE ticker = ?", (ticker.upper(),))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "ticker": row[1],
                    "type": row[2],
                    "name": row[3],
                    "sector": row[4],
                    "subsector": row[5]
                } 

            return None

    def delete(self, ticker: str):
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stocks WHERE ticker = ?", (ticker.upper(),))
            conn.commit()
            self.logger.info(f"Stock {ticker} deleted successfully")