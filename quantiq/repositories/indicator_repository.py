from quantiq.database.database import transaction
import logging

class Indicator:
    def __init__(self, stock_id: int, p_l: float, p_vp: float, p_ebit: float, psr: float, p_ativos: float, p_cap_giro: float, p_ativ_circ_liq: float, div_yield: float, ev_ebitda: float, ev_ebit: float, cres_rec_5a: float):
        self.stock_id = stock_id
        self.p_l = p_l
        self.p_vp = p_vp
        self.p_ebit = p_ebit
        self.psr = psr
        self.p_ativos = p_ativos
        self.p_cap_giro = p_cap_giro
        self.p_ativ_circ_liq = p_ativ_circ_liq
        self.div_yield = div_yield
        self.ev_ebitda = ev_ebitda
        self.ev_ebit = ev_ebit
        self.cres_rec_5a = cres_rec_5a
    
    @staticmethod
    def parse(data: dict, stock_id: int):
        for key, value in data.items():
            if value is None or value == "-":
                data[key] = None
        return Indicator(stock_id, data['p_l'], data['p_vp'], data['p_ebit'], data['psr'], data['p_ativos'], data['p_cap_giro'], data['p_ativ_circ_liq'], data['div_yield'], data['ev_ebitda'], data['ev_ebit'], data['cres_rec_5a'])

class IndicatorRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store(self, data: dict, stock_id: int):
        with transaction() as conn:
            try:
                indicators = Indicator.parse(data, stock_id)
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