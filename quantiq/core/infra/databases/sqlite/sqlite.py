from collections.abc import Generator
from contextlib import contextmanager
import logging
import sqlite3
from typing import Any

from quantiq.core.infra.databases.tables import tables
from quantiq.core.utils.project_root import get_project_root

# tables = {
#     "stocks": """
#         CREATE TABLE IF NOT EXISTS stocks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             ticker TEXT UNIQUE,
#             type TEXT NOT NULL,         -- e.g. 'stock' or 'fii'
#             name TEXT,                  -- empresa or fundo name
#             sector TEXT,
#             subsector TEXT,
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#             scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
#         );""",
#     "financial_info": """
#         CREATE TABLE IF NOT EXISTS financial_info (
#             stock_id         INTEGER    NOT NULL,
#             price            REAL       NOT NULL,    -- última cotação
#             min_52_sem       REAL       NOT NULL,
#             max_52_sem       REAL       NOT NULL,
#             last_price_date  DATETIME   NOT NULL,    -- ISO-8601 string
#             volume_by_2m     INTEGER    NOT NULL,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id)
#         );""",
#     "market_values": """
#         CREATE TABLE IF NOT EXISTS market_values (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             stock_id     INTEGER    NOT NULL,
#             identifier   TEXT       NOT NULL,        -- e.g. 'valor_de_mercado', 'ult_balanco_processado'
#             value        TEXT       DEFAULT NULL,
#             created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id, identifier)
#         );""",
#     "variations": """
#         CREATE TABLE IF NOT EXISTS variations (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             stock_id     INTEGER    NOT NULL,
#             period       TEXT       NOT NULL,        -- e.g. 'dia','m_s','30_dias','12_meses','2025',…
#             value        REAL       NOT NULL,
#             created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id, period)
#         );""",
#     "indicators": """
#         CREATE TABLE IF NOT EXISTS indicators (
#             id               INTEGER PRIMARY KEY AUTOINCREMENT,
#             stock_id         INTEGER    NOT NULL,
#             p_l              REAL,
#             p_vp             REAL,
#             p_ebit           REAL,
#             psr              REAL,
#             p_ativos         REAL,
#             p_cap_giro       REAL,
#             p_ativ_circ_liq  REAL,
#             div_yield        REAL,
#             ev_ebitda        REAL,
#             ev_ebit          REAL,
#             cres_rec_5a      REAL,
#             created_at       DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             scraped_at       DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id)
#         );""",
#     "balance_sheet": """
#         CREATE TABLE IF NOT EXISTS balance_sheet (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             stock_id     INTEGER    NOT NULL,
#             identifier   TEXT       NOT NULL,        -- e.g. 'ativo','depositos','patrim_liq', etc.
#             value        TEXT       NOT NULL,
#             created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id, identifier)
#         );""",
#     "financial_period": """
#         CREATE TABLE IF NOT EXISTS financial_period (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             stock_id     INTEGER    NOT NULL,
#             period       TEXT       NOT NULL,        -- 'last_12_months' or 'last_3_months'
#             identifier   TEXT       NOT NULL,        -- e.g. 'receita','lucro_liquido',…
#             value        TEXT       NOT NULL,
#             created_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             scraped_at   DATETIME   DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (stock_id) REFERENCES stocks(id),
#             UNIQUE(stock_id, period, identifier)
#         );""",
# }


class Sqlite:
    def __init__(self, db_name: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.db_name = db_name
        self.db_path = get_project_root() / db_name

    """
    Create the database.

    Args:
        db_name: The name of the database.
    """

    @staticmethod
    def create_database(db_name: str = "quantiq.db") -> None:
        db_path = get_project_root() / db_name
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(tables[table])
        conn.commit()
        conn.close()

    """
    Transaction context manager.
    """

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        except Exception as e:
            self.logger.error(f"Error in transaction: {e}")
            raise e
        finally:
            conn.close()

    def upsert(self, query: str, params: Any | None = None) -> int:
        with self.transaction() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or {})
                cursor.close()
                conn.commit()
                lastrowid = cursor.lastrowid
                if lastrowid is None:
                    return 0
                return lastrowid
            except Exception as e:
                self.logger.error(f"Error in upsert: {e}")
                conn.rollback()
                raise e

    def fetch_all(self, query: str, params: Any | None = None) -> list[Any]:
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Any | None = None) -> Any | None:
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            return cursor.fetchone()
