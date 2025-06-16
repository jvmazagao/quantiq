from typing import Any


class Stock:
    def __init__(
        self,
        ticker: str,
        type: str,
        name: str,
        sector: str | None = None,
        subsector: str | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.name = name
        self.sector = sector
        self.subsector = subsector

    @staticmethod
    def parse(data: dict[str, Any]) -> "Stock":
        if "fii" in data:
            return Stock(
                ticker=str(data.get("fii", "")),
                type=str(data.get("tipo", "")),
                name=str(data.get("nome", "")),
                sector=str(data.get("segmento", "")) if data.get("segmento") else None,
            )

        return Stock(
            ticker=str(data.get("papel", "")),
            type=str(data.get("tipo", "")),
            name=str(data.get("empresa", "")),
            sector=str(data.get("setor", "")) if data.get("setor") else None,
            subsector=str(data.get("subsetor", "")) if data.get("subsetor") else None,
        )
