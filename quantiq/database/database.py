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
            type TEXT NOT NULL,         -- e.g. 'stock' or 'fii'
            name TEXT,                  -- empresa or fundo name
            sector TEXT,
            subsector TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );""",

    "financial_info": """
        CREATE TABLE IF NOT EXISTS financial_info (
            stock_id         INTEGER    NOT NULL,
            price            REAL       NOT NULL,    -- última cotação
            min_52_sem       REAL       NOT NULL,
            max_52_sem       REAL       NOT NULL,
            last_price_date  DATETIME   NOT NULL,    -- ISO-8601 string
            volume_by_2m     INTEGER    NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id)
        );""",

    "market_values": """
        CREATE TABLE IF NOT EXISTS market_values (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id     INTEGER    NOT NULL,
            identifier   TEXT       NOT NULL,        -- e.g. 'valor_de_mercado', 'ult_balanco_processado'
            value        TEXT       DEFAULT NULL,
            created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id, identifier)
        );""",

    "variations": """
        CREATE TABLE IF NOT EXISTS variations (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id     INTEGER    NOT NULL,
            period       TEXT       NOT NULL,        -- e.g. 'dia','m_s','30_dias','12_meses','2025',…
            value        REAL       NOT NULL,
            created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id, period)
        );""",

    "indicators": """
        CREATE TABLE IF NOT EXISTS indicators (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id         INTEGER    NOT NULL,
            p_l              REAL,
            p_vp             REAL,
            p_ebit           REAL,
            psr              REAL,
            p_ativos         REAL,
            p_cap_giro       REAL,
            p_ativ_circ_liq  REAL,
            div_yield        REAL,
            ev_ebitda        REAL,
            ev_ebit          REAL,
            cres_rec_5a      REAL,
            created_at       DATETIME   DEFAULT CURRENT_TIMESTAMP,
            scraped_at       DATETIME   DEFAULT CURRENT_TIMESTAMP,
            ffo_yield        REAL,
            ffo_cota         REAL,
            dividendo_cota   REAL,
            vp_cota          REAL,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id)
        );""",

    "balance_sheet": """
        CREATE TABLE IF NOT EXISTS balance_sheet (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id     INTEGER    NOT NULL,
            identifier   TEXT       NOT NULL,        -- e.g. 'ativo','depositos','patrim_liq', etc.
            value        TEXT       NOT NULL,
            created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id, identifier)
        );""",

    "financial_period": """
        CREATE TABLE IF NOT EXISTS financial_period (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id     INTEGER    NOT NULL,
            period       TEXT       NOT NULL,        -- 'last_12_months' or 'last_3_months'
            identifier   TEXT       NOT NULL,        -- e.g. 'receita','lucro_liquido',…
            value        TEXT       NOT NULL,
            created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stock_id) REFERENCES stocks(id),
            UNIQUE(stock_id, period, identifier)
        );"""
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
