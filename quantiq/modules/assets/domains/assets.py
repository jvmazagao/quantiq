from enum import Enum
from typing import Any

from pydantic import Field

from quantiq.core.domain.base import Base


class AssetType(Enum):
    STOCK = "stock"
    FII = "fii"


class Asset(Base):
    ticker: str = Field(description="Ticker of the asset")
    type: AssetType = Field(description="Type of the asset")
    name: str = Field(description="Name of the asset")

    @classmethod
    def create(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            **data,
        )
