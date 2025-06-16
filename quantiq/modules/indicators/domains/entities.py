from typing import Any


class Indicator:
    def __init__(
        self,
        stock_id: int,
        p_l: float | None,
        p_vp: float | None,
        p_ebit: float | None,
        psr: float | None,
        p_ativos: float | None,
        p_cap_giro: float | None,
        p_ativ_circ_liq: float | None,
        div_yield: float | None,
        ev_ebitda: float | None,
        ev_ebit: float | None,
        cres_rec_5a: float | None,
    ) -> None:
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
    def parse(data: dict[str, Any], stock_id: int) -> "Indicator":
        return Indicator(
            stock_id,
            data.get("p_l"),
            data.get("p_vp"),
            data.get("p_ebit"),
            data.get("psr"),
            data.get("p_ativos"),
            data.get("p_cap_giro"),
            data.get("p_ativ_circ_liq"),
            data.get("div_yield"),
            data.get("ev_ebitda"),
            data.get("ev_ebit"),
            data.get("cres_rec_5a"),
        )
