from quantiq.database.database import transaction
import logging
from quantiq.modules.indicators.domains.entities import Indicator

class IndicatorRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, indicators: Indicator):
        with transaction() as conn:
            try:
                values = (indicators.stock_id, indicators.p_l, indicators.p_vp, indicators.p_ebit, indicators.psr, indicators.p_ativos, indicators.p_cap_giro, indicators.p_ativ_circ_liq, indicators.div_yield, indicators.ev_ebitda, indicators.ev_ebit, indicators.cres_rec_5a)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO indicators (stock_id, p_l, p_vp, p_ebit, psr, p_ativos, p_cap_giro, p_ativ_circ_liq, div_yield, ev_ebitda, ev_ebit, cres_rec_5a)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (stock_id) DO UPDATE SET p_l = excluded.p_l, p_vp = excluded.p_vp, p_ebit = excluded.p_ebit, psr = excluded.psr, p_ativos = excluded.p_ativos, p_cap_giro = excluded.p_cap_giro, p_ativ_circ_liq = excluded.p_ativ_circ_liq, div_yield = excluded.div_yield, ev_ebitda = excluded.ev_ebitda, ev_ebit = excluded.ev_ebit, cres_rec_5a = excluded.cres_rec_5a
                """, values)
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                self.logger.error(f"Error storing indicator: {e}")
                conn.rollback()
                raise e 