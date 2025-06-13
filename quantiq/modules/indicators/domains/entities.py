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
        return Indicator(stock_id, data.get('p_l', None), data.get('p_vp', None), data.get('p_ebit', None), data.get('psr', None), data.get('p_ativos', None), data.get('p_cap_giro', None), data.get('p_ativ_circ_liq', None), data.get('div_yield', None), data.get('ev_ebitda', None), data.get('ev_ebit', None), data.get('cres_rec_5a', None)) 