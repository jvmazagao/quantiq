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
