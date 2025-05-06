import sqlite3
from pathlib import Path
import logging
from contextlib import contextmanager
logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "quantiq.db"

tables = {
    "stocks": """
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            type TEXT,
            name TEXT,
            sector TEXT,
            subsector TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""",
    "financial_info": """
        CREATE TABLE IF NOT EXISTS financial_info (
            stock_id         INTEGER    NOT NULL,
            price            REAL       NOT NULL,
            min_52_sem         REAL       NOT NULL,
            max_52_sem         REAL       NOT NULL,
            last_price_date       DATETIME       NOT NULL,    -- ISO-8601: '2025-05-02T00:00:00Z'
            volume_by_2m         INTEGER    NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id)
        )""",
    "market_values": """
        CREATE TABLE IF NOT EXISTS market_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            value TEXT,
            identifier TEXT,
            FOREIGN KEY (stock_id) REFERENCES stocks (id)
        )""",
    "variations": """
        CREATE TABLE IF NOT EXISTS variations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            period TEXT,
            value TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks (id),
            UNIQUE(stock_id, period)
        )""",
    "indicators": """
        CREATE TABLE IF NOT EXISTS indicators (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id           INTEGER NOT NULL,
            p_l                REAL ,               
            p_vp               REAL,               
            p_ebit             REAL,               
            psr                REAL,               
            p_ativos           REAL,               
            p_cap_giro         REAL,               
            p_ativ_circ_liq    REAL,               
            div_yield          REAL,               
            ev_ebitda          REAL,               
            ev_ebit            REAL,               
            cres_rec_5a        REAL,   
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id)
        ); """,
    "balance_sheet": """
        CREATE TABLE IF NOT EXISTS balance_sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            identifier TEXT,
            value TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks (id),
            UNIQUE(stock_id, identifier)
        )""",
    "income_statement": """
        CREATE TABLE IF NOT EXISTS financial_period (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id         INTEGER NOT NULL,
            period           TEXT    NOT NULL,
            identifier       TEXT    NOT NULL,
            value           TEXT    NOT NULL,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(stock_id, period, identifier),
            FOREIGN KEY (stock_id) REFERENCES stocks(id)
        )"""           
}

def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in tables:
        c.execute(tables[table])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

def insert_stock(conn, stock_data):
    """Insert a stock into the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (ticker, type, name, sector, subsector)
            VALUES (?, ?, ?, ?, ?)
        """, (stock_data["ticker"], stock_data["type"], stock_data["name"], stock_data["sector"], stock_data["subsector"]))
        conn.commit()
        logger.info(f"Stock {stock_data['ticker']} inserted successfully")
        return { 'id': cursor.lastrowid, 'ticker': stock_data['ticker'] }
    except sqlite3.Error as e:
        if isinstance(e, sqlite3.IntegrityError):
            logger.error(f"Stock {stock_data['ticker']} already exists")
            return fetch_stock(conn, stock_data["ticker"])
        logger.error(f"Error inserting stock {stock_data['ticker']}: {e}")
        conn.rollback()
        raise e

def insert_financial_info(conn, financial_info_data):
    """Insert financial info into the database."""
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO financial_info (stock_id, identifier, value)
            VALUES (?, ?, ?)
        """
        values = []
        for key, value in financial_info_data.items():
            values.append((financial_info_data["stock_id"], key, value))
        cursor.executemany(query, values)
        conn.commit()
        logger.info(f"Financial info for {financial_info_data['stock_id']} inserted successfully")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Error inserting financial info for {financial_info_data['stock_id']}: {e}")
        conn.rollback()

def fetch_financial_info(conn, ticker):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financial_info WHERE ticker = ?", (ticker.upper(),))
    row = cursor.fetchone()
    if row:
        return {
            "id": row[0],
            "ticker": row[1],
            "current_value": row[2],
            "min_52_sem": row[3],
            "max_52_sem": row[4],
            "data_ult_cot": row[5],
            "vol_med_2m": row[6]
        }
    return None


def fetch_stock(conn, ticker):
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

def delete_stock(conn, ticker):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stocks WHERE ticker = ?", (ticker.upper(),))
    conn.commit()
    logger.info(f"Stock {ticker} deleted successfully")

@contextmanager
def transaction(path = DB_PATH):
    conn = sqlite3.connect(path)
    try:
        yield conn
    except Exception as e:
        logger.error(f"Error in transaction: {e}")
        raise e
    finally:
        conn.close()
