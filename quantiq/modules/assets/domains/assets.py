from dataclasses import dataclass
from enum import Enum
from typing import Any

from quantiq.core.domain.base import Base


class AssetType(Enum):
    STOCK = "stock"
    FII = "fii"


@dataclass
class Asset(Base):
    ticker: str
    type: AssetType
    name: str
    id: int | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            ticker=str(data.get("ticker", "")),
            type=AssetType(str(data.get("type", ""))),
            name=str(data.get("name", "")),
        )
