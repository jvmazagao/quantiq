import logging

from quantiq.database.database import transaction
from quantiq.modules.indicators.domains.entities import Indicator


class IndicatorRepository:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def store(self, indicators: Indicator) -> int:
        with transaction() as conn:
            try:
                values = (
                    indicators.stock_id,
                    indicators.p_l,
                    indicators.p_vp,
                    indicators.p_ebit,
                    indicators.psr,
                    indicators.p_ativos,
                    indicators.p_cap_giro,
                    indicators.p_ativ_circ_liq,
                    indicators.div_yield,
                    indicators.ev_ebitda,
                    indicators.ev_ebit,
                    indicators.cres_rec_5a,
                )
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO indicators (stock_id, p_l, p_vp, p_ebit, psr, p_ativos, p_cap_giro, p_ativ_circ_liq, div_yield, ev_ebitda, ev_ebit, cres_rec_5a)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (stock_id) DO UPDATE SET p_l = excluded.p_l, p_vp = excluded.p_vp, p_ebit = excluded.p_ebit, psr = excluded.psr, p_ativos = excluded.p_ativos, p_cap_giro = excluded.p_cap_giro, p_ativ_circ_liq = excluded.p_ativ_circ_liq, div_yield = excluded.div_yield, ev_ebitda = excluded.ev_ebitda, ev_ebit = excluded.ev_ebit, cres_rec_5a = excluded.cres_rec_5a
                """,
                    values,
                )
                conn.commit()
                return cursor.lastrowid  # type: ignore
            except Exception as e:
                self.logger.error(f"Error storing indicator: {e}")
                conn.rollback()
                raise e

    def fetch(self, stock_id: int) -> Indicator | None:
        with transaction() as conn:
            cursor = conn.cursor()
            row = cursor.execute(
                "SELECT stock_id, p_l, p_vp, p_ebit, psr, p_ativos, p_cap_giro, p_ativ_circ_liq, div_yield, ev_ebitda, ev_ebit, cres_rec_5a FROM indicators WHERE stock_id = ?",
                (stock_id,),
            ).fetchone()

            if not row:
                return None

            return Indicator(
                stock_id=row[0],
                p_l=row[1],
                p_vp=row[2],
                p_ebit=row[3],
                psr=row[4],
                p_ativos=row[5],
                p_cap_giro=row[6],
                p_ativ_circ_liq=row[7],
                div_yield=row[8],
                ev_ebitda=row[9],
                ev_ebit=row[10],
                cres_rec_5a=row[11],
            )
