from datetime import datetime

from pydantic import Field

from quantiq.core.domain.base import Base


class AssetDetails(Base):
    governance: str | None = Field(description="Governance of the asset", default=None)
    sector: str | None = Field(description="Sector of the asset", default=None)
    subsector: str | None = Field(description="Subsector of the asset", default=None)
    market_value: int | None = Field(
        description="Market value of the asset", default=None
    )
    last_balance_proccessed: datetime | None = Field(
        description="Last balance proccessed of the asset", default=None
    )
    company_value: int | None = Field(
        description="Company value of the asset", default=None
    )
    number_of_stocks: int | None = Field(
        description="Stock number of the asset", default=None
    )
    asset_id: int | None = Field(description="Asset ID of the asset", default=None)

    class Config:
        extra = "ignore"
