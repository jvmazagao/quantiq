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