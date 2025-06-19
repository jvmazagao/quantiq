# type: ignore-all

import contextlib
import logging
import re
from typing import Any

from bs4 import BeautifulSoup
import requests

from quantiq.modules.scrapper.providers.fundamentus.data import REITDetails
from quantiq.modules.scrapper.providers.scrapper import Scrapper

logger = logging.getLogger(__name__)


class FundamentusREITScraper(Scrapper):
    def __init__(self) -> None:
        super().__init__("reits")
        self.base_url = "https://www.fundamentus.com.br/detalhes.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _extract_basic_info(self, soup: BeautifulSoup) -> dict[str, Any]:
        """Extrai a tabela principal de informações básicas e cotação."""
        table = soup.find_all("table")[0]
        rows = table.find_all("tr")  # type: ignore
        basic_info = {}
        cotacao_info = {}
        for row in rows:
            cols = row.find_all(["td", "th"])  # type: ignore
            if len(cols) == 4:
                k1, v1, k2, v2 = (c.get_text(strip=True) for c in cols)
                k1 = self._format_key(k1)
                k2 = self._format_key(k2)
                if k1:
                    basic_info[k1] = self._parse_value(v1)
                if k2 in [
                    "cotacao",
                    "data_ult_cot",
                    "min_52_sem",
                    "max_52_sem",
                    "vol_med_2m",
                ]:
                    cotacao_info[k2] = self._parse_value(v2)
            elif len(cols) == 2:
                k, v = (c.get_text(strip=True) for c in cols)
                k = self._format_key(k)
                if k in [
                    "cotacao",
                    "data_ult_cot",
                    "min_52_sem",
                    "max_52_sem",
                    "vol_med_2m",
                ]:
                    cotacao_info[k] = self._parse_value(v)
                else:
                    basic_info[k] = self._parse_value(v)
        basic_info["tipo"] = "reit"
        if cotacao_info:
            basic_info["cotacao"] = cotacao_info
        return basic_info

    def _extract_oscilations(self, soup):
        """Extrai a coluna de Oscilações da tabela correspondente."""
        # Procura a tabela que contém 'Oscilações' no cabeçalho
        for table in soup.find_all("table"):
            header = table.find("tr")
            if header and "Oscilações" in header.get_text():
                rows = table.find_all("tr")[1:]  # pula o cabeçalho
                oscilations = {}
                for row in rows:
                    cols = row.find_all(["td", "th"])  # type: ignore
                    if len(cols) >= 2:
                        k = self._format_key(cols[0].get_text(strip=True))
                        v = self._parse_value(cols[1].get_text(strip=True))
                        if k:
                            oscilations[k] = v
                return oscilations
        return {}

    def _extract_indicadores(self, soup):
        """Extrai os indicadores (lado direito da tabela Indicadores) de forma simples."""
        for table in soup.find_all("table"):
            header = table.find("tr")
            if header and "Indicadores" in header.get_text():
                indicadores = {}
                for tr in table.find_all("tr"):
                    cells = [
                        cell.get_text(strip=True)
                        for cell in tr.find_all(["th", "td"])  # type: ignore
                    ]
                    if len(cells) >= 4:
                        key = cells[2]
                        val = cells[3]
                        key = self._format_key(key)
                        with contextlib.suppress(Exception):
                            val = self._parse_value(val)
                        indicadores[key] = val
                return indicadores
        return {}

    def oscillations_to_dict(self, rows: list[list[str]]) -> dict:
        oscillations = {}
        indicators = {}
        for r in rows[1:4]:
            period = self._format_key(r[0])
            oscillations[period] = self._parse_value(r[1])
            for i in range(2, len(r), 2):
                name = self._format_key(r[i])
                val = self._parse_value(r[i + 1])
                indicators[name] = val

        raw = rows[4]
        for i, cell in enumerate(raw):
            if cell == "12 meses" or re.match(r"^\d{4}$", cell):
                period = self._format_key(cell)
                oscillations[period] = self._parse_value(raw[i + 1])

        metrics_rows = [
            r for r in rows[5:] if len(r) >= 6 and r[0] and r[2].startswith("?")
        ]
        m12 = {}
        m3 = {}
        for r in metrics_rows:
            name = self._format_key(r[2])
            val12 = self._parse_value(r[3])
            val3 = self._parse_value(r[5])
            m12[name] = val12
            m3[name] = val3
        indicators_by_period = {"last_12_months": m12, "last_3_months": m3}

        bs_idx = next(i for i, r in enumerate(rows) if "Balanço Patrimonial" in r)
        this_row = rows[bs_idx]
        part1 = this_row[this_row.index("Balanço Patrimonial") + 1 :]
        flat = [x for x in (part1) if x]
        bs_data = {
            self._format_key(flat[i]): self._parse_value(flat[i + 1])
            for i in range(0, len(flat), 2)
        }

        return {
            "oscillations": oscillations,
            "indicators": indicators,
            "indicators_by_period": indicators_by_period,
            "balance_sheet": bs_data,
        }

    def scrape(self, ticker: str) -> dict:
        """Extracts all main sections as arrays of row arrays and returns basic_info_dict from the first row."""
        logger.info(f"Scraping REIT data for {ticker}")
        response = requests.get(f"{self.base_url}?papel={ticker}", headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if self._is_reit_not_found(soup):
            raise Exception(f"REIT with ticker {ticker} not found on Fundamentus")

        basic_info = self._table_rows_to_dict(
            self._extract_table_rows_by_header(soup, "FII")
        )

        last_financial_keys = [
            "cotacao",
            "min_52_sem",
            "max_52_sem",
            "data_ult_cot",
            "vol_med_2m",
        ]

        last_financial_info = {
            k: basic_info.pop(k) for k in last_financial_keys if k in basic_info
        }

        oscillations_dict = self.oscillations_to_dict(
            self._extract_table_rows_by_header(soup, "Oscilações")
        )

        properties_dict = self._table_rows_to_dict(
            self._extract_table_rows_by_header(soup, "Imóveis")
        )

        data = {
            **basic_info,
            "last_financial_info": last_financial_info,
            "market_values": properties_dict,
            "variations": oscillations_dict.get("oscillations", {}),
            "indicators": oscillations_dict.get("indicators", {}),
            "balance_sheet": oscillations_dict.get("balance_sheet", {}),
            "financial_results": oscillations_dict.get("indicators_by_period", {}),
        }

        return REITDetails.create(data).model_dump()

    def _is_reit_not_found(self, soup: BeautifulSoup) -> bool:
        """Check if the REIT was not found on Fundamentus."""
        error_message = soup.find("div", {"class": "error"})
        if error_message and "papel não encontrado" in error_message.text.lower():
            return True
        return False

    def _parse_variations_and_indicators(
        self, rows: list[list[str]]
    ) -> tuple[dict, dict]:
        variations = {}
        indicators = {}
        for row in rows[1:]:
            var_key = row[0].strip()
            var_value = row[1].strip()
            if var_key and var_key not in ["Oscilações", ""]:
                variations[var_key] = var_value
            ind_key = row[2].replace("?", "").strip()
            ind_value = row[3].strip()
            if ind_key and ind_key not in ["Indicadores", ""]:
                indicators[ind_key] = ind_value
        return variations, indicators
