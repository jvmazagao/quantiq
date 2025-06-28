from datetime import datetime
from typing import Any

from pydantic import Field

from quantiq.core.domain.base import Base
from quantiq.modules.scrapper.providers.fundamentus.data import AssetType


class Asset(Base):
    ticker: str = Field(description="Ticker of the asset")
    type: AssetType = Field(description="Type of the asset")
    name: str = Field(description="Name of the asset")

    class Config:
        extra = "ignore"

    @classmethod
    def create(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            **data,
        )


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
