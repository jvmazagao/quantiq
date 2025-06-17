from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Any
import unicodedata


class Scrapper(ABC):
    type: str

    def __init__(self, type: str) -> None:
        self.type = type

    @abstractmethod
    def scrape(self, ticker: str) -> dict[str, Any]:
        pass

    def _to_snake_case(self, s: str) -> str:
        if not s:
            return s

        # Normalize unicode and remove accents
        s = unicodedata.normalize("NFD", s.lower())
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")

        # Replace non-alphanumeric with underscore and clean up
        s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
        return s

    def _parse_value(self, value: str) -> float | int | str | None:
        if value is None or value.strip() == "-":
            return None

        v = value.strip().replace(".", "").replace(" ", "")

        date_match = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", value.strip())

        if date_match:
            try:
                dt = datetime.strptime(value.strip(), "%d/%m/%Y")
                return dt.strftime("%Y-%m-%dT00:00:00Z")
            except Exception:
                pass

        if v.endswith("%"):
            try:
                return float(v[:-1].replace(",", "."))
            except Exception:
                return value

        if v.isdigit():
            try:
                return int(v)
            except Exception:
                return value

        try:
            return float(v.replace(",", "."))
        except Exception:
            return value

    def _table_rows_to_dict(self, rows: list[list[str]]) -> dict:
        d = {}
        for r in rows:
            for i in range(0, len(r) - 1, 2):
                k = self._to_snake_case(r[i])
                v = self._parse_value(r[i + 1])
                if k and v is not None:
                    d[k] = v
        return d
