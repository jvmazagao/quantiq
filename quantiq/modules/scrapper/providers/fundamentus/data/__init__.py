from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pydantic.aliases import AliasChoices


class Base(BaseModel):
    @model_validator(mode="before")
    def clean_up_empty_fields(cls, values: Any) -> dict[str, Any]:
        return {k: v for k, v in values.items() if v is not None}

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        return {k: v for k, v in data.items() if v is not None}


class Details(Base):
    ticker: str = Field(alias="papel")
    name: str = Field(alias="empresa")


class Asset(Base):
    price: float = Field(alias="cotacao")
    last_price_update: datetime = Field(alias="data_ult_cot")
    fifty_two_week_low: float = Field(alias="min_52_sem")
    fifty_two_week_high: float = Field(alias="max_52_sem")
    avg_volume_2m: int = Field(alias="vol_med_2m")

    @classmethod
    def create(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            **data,
        )


class PropertyMetrics(Base):
    property_count: int | None = Field(alias="qtd_imoveis", default=None)
    total_area_sqm: int | None = Field(alias="area_m2", default=None)
    unit_count: int | None = Field(alias="qtd_unidades", default=None)

    cap_rate: float | None = Field(alias="cap_rate", default=None)
    avg_vacancy_rate: float | None = Field(alias="vacancia_media", default=None)
    rent_per_sqm: float | None = Field(alias="aluguel_m2", default=None)

    price_per_sqm: float | None = Field(alias="preco_do_m2", default=None)
    portfolio_allocation: float | None = Field(alias="imoveis_pl_do_fii", default=None)


class YearlyVariation(Base):
    year: int
    variation: float | None = None


class Variations(Base):
    day: float = Field(alias="dia")
    month: float = Field(alias="mes")
    thirty_days: float = Field(alias="30_dias")
    twelve_months: float = Field(alias="12_meses")
    yearly_variations: list[YearlyVariation] = Field(default_factory=list)

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",  # Changed to forbid to prevent issues
    )

    @model_validator(mode="before")
    @classmethod
    def extract_yearly_variations(cls, values: Any) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values

        # Create a copy to avoid modifying original
        values_copy = values.copy()
        fixed_keys = {
            "dia",
            "mes",
            "30_dias",
            "12_meses",
        }

        yearly_variations = []
        fields_to_remove = []

        for key, value in values_copy.items():
            if key not in fixed_keys:
                if isinstance(value, str):
                    fields_to_remove.append(key)
                    continue

                if (
                    str(key).isdigit()
                    and len(str(key)) == 4
                    and 1900 <= int(key) <= 2100
                ):
                    yearly_variations.append(
                        YearlyVariation(
                            year=int(key),
                            variation=float(value) if value is not None else None,
                        )
                    )

                fields_to_remove.append(key)

        for key in fields_to_remove:
            values_copy.pop(key, None)

        yearly_variations.sort(key=lambda x: x.year, reverse=True)
        values_copy["yearly_variations"] = [
            var.model_dump() for var in yearly_variations
        ]

        return values_copy


class Indicators(Base):
    dividend_yield: float = Field(alias="div_yield")
    price_to_book_ratio: float = Field(alias="p_vp")


class ReitIndicators(Base):
    ffo_yield: float = Field(alias="ffo_yield", description="FFO Yield (%)")
    ffo_per_share: float = Field(alias="ffo_cota", description="FFO per Share")

    # Dividend Metrics
    dividend_yield: float = Field(alias="div_yield", description="Dividend Yield (%)")
    dividend_per_share: float = Field(
        alias="dividendo_cota", description="Dividend per Share"
    )

    # Valuation Metrics
    pb_ratio: float = Field(alias="p_vp", description="Price-to-Book ratio")
    book_value_per_share: float = Field(
        alias="vp_cota", description="Book Value per Share"
    )

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class StockIndicators(Base):
    # Valuation Ratios
    pe_ratio: float | None = Field(
        alias="p_l", description="Price-to-Earnings ratio", default=None
    )
    eps: float | None = Field(
        alias="lpa", description="Earnings Per Share", default=None
    )
    pb_ratio: float | None = Field(
        alias="p_vp", description="Price-to-Book ratio", default=None
    )
    book_value_per_share: float | None = Field(
        alias="vpa", description="Book Value Per Share", default=None
    )
    price_to_ebit: float | None = Field(
        alias="p_ebit", description="Price-to-EBIT ratio", default=None
    )
    ps_ratio: float | None = Field(
        alias="psr", description="Price-to-Sales ratio", default=None
    )
    price_to_assets: float | None = Field(
        alias="p_ativos", description="Price-to-Assets ratio", default=None
    )
    price_to_working_capital: float | None = Field(
        alias="p_cap_giro", description="Price-to-Working Capital", default=None
    )
    price_to_net_current_assets: float | None = Field(
        alias="p_ativ_circ_liq", description="Price-to-Net Current Assets", default=None
    )

    # Profitability Margins (%)
    gross_margin: float | None = Field(
        alias="marg_bruta", description="Gross Margin (%)", default=None
    )
    ebit_margin: float | None = Field(
        alias="marg_ebit", description="EBIT Margin (%)", default=None
    )
    net_margin: float | None = Field(
        alias="marg_liquida", description="Net Margin (%)", default=None
    )

    # Return Metrics (%)
    roic: float | None = Field(
        alias="roic", description="Return on Invested Capital (%)", default=None
    )
    roe: float | None = Field(
        alias="roe", description="Return on Equity (%)", default=None
    )
    ebit_to_assets: float | None = Field(
        alias="ebit_ativo", description="EBIT to Assets (%)", default=None
    )

    # Dividend & Growth
    revenue_growth_5y: float | None = Field(
        alias="cres_rec_5a", description="5-Year Revenue Growth (%)", default=None
    )

    # Enterprise Value Ratios
    ev_ebitda: float | None = Field(
        alias="ev_ebitda", description="Enterprise Value to EBITDA", default=None
    )
    ev_ebit: float | None = Field(
        alias="ev_ebit", description="Enterprise Value to EBIT", default=None
    )

    # Financial Health
    current_ratio: float | None = Field(
        alias="liquidez_corr", description="Current Ratio", default=None
    )
    debt_to_equity: float | None = Field(
        alias="div_br_patrim", description="Debt-to-Equity ratio", default=None
    )
    asset_turnover: float | None = Field(
        alias="giro_ativos", description="Asset Turnover", default=None
    )

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class BalanceSheet(Base):
    """REIT Balance Sheet data"""

    total_assets: int | None = Field(
        alias="ativos", description="Total Assets", default=None
    )
    shareholders_equity: int | None = Field(
        alias="patrim_liquido", description="Shareholders Equity", default=None
    )

    model_config = ConfigDict(populate_by_name=True)


class PeriodResults(Base):
    """Financial results for a specific period"""

    revenue: int | None = Field(
        alias=AliasChoices("receita", "receita_liquida"),
        description="Revenue",
        default=None,
    )  # type: ignore
    asset_sales: int | None = Field(
        alias="venda_de_ativos", description="Asset Sales", default=None
    )
    ffo: int | None = Field(
        alias="ffo", description="Funds From Operations", default=None
    )
    distributions: int | None = Field(
        alias="rend_distribuido", description="Distributions Paid", default=None
    )

    ebit: int | None = Field(alias="ebit", description="EBIT", default=None)

    finance_revenue_intermediate: int | None = Field(
        alias="result_int_financ",
        description="Intermediate Finance Revenue",
        default=None,
    )
    service_revenue: int | None = Field(
        alias="rec_servicos", description="Service Revenue", default=None
    )
    net_revenue: int | None = Field(
        alias="lucro_liquido", description="Net Revenue", default=None
    )

    model_config = ConfigDict(populate_by_name=True)


class FinancialResults(Base):
    """REIT Financial Results"""

    last_12_months: PeriodResults = Field(alias="last_12_months")
    last_3_months: PeriodResults = Field(alias="last_3_months")

    model_config = ConfigDict(populate_by_name=True)


class StockBalanceSheet(BalanceSheet):
    gross_debt: int | None = Field(
        alias="div_bruta", description="Gross Debt", default=None
    )
    cash_and_equivalents: int | None = Field(
        alias="disponibilidades", description="Cash and Cash Equivalents", default=None
    )
    net_debt: float | None = Field(
        alias="div_liquida", description="Net Debt", default=None
    )
    current_assets: int | None = Field(
        alias="ativo_circulante", description="Current Assets", default=None
    )

    deposits: int | None = Field(
        alias="depositos", description="Deposits", default=None
    )
    credit_cards: int | None = Field(
        alias="cart_de_credito", description="Credit Cards", default=None
    )

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class REITDetails(Details):
    segment: str = Field(alias="segmento")
    management: str = Field(alias="mandato")
    investment_strategy: str = Field(alias="gestao")

    asset: Asset = Field(alias="last_financial_info")
    property_metrics: PropertyMetrics = Field(alias="market_values")
    variations: Variations = Field(alias="variations")
    indicators: ReitIndicators = Field(alias="indicators")
    balance_sheet: BalanceSheet = Field(alias="balance_sheet")
    financial_results: FinancialResults = Field(alias="financial_results")

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @model_validator(mode="before")
    def clean_up_empty_fields(cls, values: Any) -> dict[str, Any]:
        return {k: v for k, v in values.items() if v is not None}


class StockDetails(Details):
    governance: str = Field(alias="tipo")
    sector: str = Field(alias="setor")
    subsector: str = Field(alias="subsetor")
    market_value: int = Field(alias="valor_de_mercado")
    last_balance_proccessed: datetime = Field(alias="ult_balanco_processado")
    company_value: int | None = Field(alias="valor_da_firma", default=None)
    stock_number: int = Field(alias="nro_acoes")

    asset: Asset = Field(alias="last_financial_info")
    variations: Variations = Field(alias="variations")
    indicators: StockIndicators = Field(alias="indicators")
    balance_sheet: StockBalanceSheet = Field(alias="balance_sheet")
    financial_results: FinancialResults = Field(alias="financial_results")

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @model_validator(mode="before")
    def clean_up_empty_fields(cls, values: Any) -> dict[str, Any]:
        return {k: v for k, v in values.items() if v is not None}

    @classmethod
    def create(cls, data: dict[str, Any]) -> "StockDetails":
        return cls(
            **data,
        )
