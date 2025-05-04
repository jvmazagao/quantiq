import logging
from datetime import datetime

from quantiq.database.database import transaction

class FinancialInfo:
    def __init__(self, 
                 stock_id: int, 
                 price: float, 
                 min_52_sem: float, 
                 max_52_sem: float, 
                 last_price_date: datetime, 
                 volume_by_2m: int, 
                 id: int = None):
        self.id = id
        self.stock_id = stock_id
        self.price = price
        self.min_52_sem = min_52_sem
        self.max_52_sem = max_52_sem
        self.last_price_date = last_price_date
        self.volume_by_2m = volume_by_2m
        
    @staticmethod
    def parse(data: dict, stock_id: int):
        return FinancialInfo(
            stock_id, 
            data['cotacao'], 
            data['min_52_sem'], 
            data['max_52_sem'], 
            data['data_ult_cot'], 
            data['vol_med_2m'])

class FinancialInfoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, financial_info: dict, stock_id: int):
        with transaction() as conn:
            try:
                financial_info = FinancialInfo.parse(financial_info, stock_id)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO financial_info (stock_id, price, min_52_sem, max_52_sem, last_price_date, volume_by_2m)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT (stock_id) DO UPDATE SET price = excluded.price, min_52_sem = excluded.min_52_sem, max_52_sem = excluded.max_52_sem, last_price_date = excluded.last_price_date, volume_by_2m = excluded.volume_by_2m
                """, (financial_info.stock_id, financial_info.price, financial_info.min_52_sem, financial_info.max_52_sem, financial_info.last_price_date, financial_info.volume_by_2m))
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                self.logger.error(f"Error storing financial info: {e}")
                conn.rollback()
                raise e
            
    def fetch_by_stock_id(self, stock_id: int):
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM financial_info WHERE stock_id = ?", (stock_id,))
            return cursor.fetchall()
    
    def delete(self, stock_id: int):
        with transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM financial_info WHERE stock_id = ?", (stock_id,))
            conn.commit()
            self.logger.info(f"Financial info for stock {stock_id} deleted successfully")
