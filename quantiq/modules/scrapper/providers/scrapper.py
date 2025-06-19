from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Any
import unicodedata

from bs4 import BeautifulSoup


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

        s = unicodedata.normalize("NFD", s.lower())
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")

        s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
        return s

    def _parse_value(self, value: str) -> float | int | str | None:
        if value is None or value == "-" or value == "":
            return None

        v = str(value).strip().replace(".", "").replace(" ", "")

        date_match = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", v)

        if date_match:
            try:
                dt = datetime.strptime(v, "%d/%m/%Y")
                return dt.strftime("%Y-%m-%dT00:00:00Z")
            except Exception:
                pass

        if v.endswith("%"):
            try:
                return float(v[:-1].replace(",", "."))
            except Exception:
                return value

        if "," in v:
            try:
                return float(v.replace(",", "."))
            except Exception:
                return value

        if v.isdigit():
            try:
                return int(v)
            except Exception:
                return value

        try:
            return float(v)
        except Exception:
            return value

    def _table_rows_to_dict(self, rows: list[list[str]]) -> dict:
        d = {}
        for r in rows:
            for i in range(0, len(r) - 1, 2):
                k = self._format_key(r[i])
                v = self._parse_value(r[i + 1])
                if k and v is not None:
                    d[k] = v
        return d

    def _format_key(self, k: str) -> str:
        if not k:
            return k

        return self._to_snake_case(k.replace("?", "").strip())

    def _clean_keys(self, d: dict) -> dict:
        return {self._format_key(k): v for k, v in d.items() if k}

    def _extract_table_rows_by_header(
        self, soup: BeautifulSoup, header_text: str
    ) -> list[list[str]]:
        for table in soup.find_all("table"):
            header = table.find("tr")  # type: ignore
            if header and header_text in header.get_text():  # type: ignore
                rows = []
                for tr in table.find_all("tr"):  # type: ignore
                    cells = [
                        cell.get_text(strip=True)
                        for cell in tr.find_all(["th", "td"])  # type: ignore
                    ]
                    if cells:
                        rows.append(cells)
                return rows
        return []
