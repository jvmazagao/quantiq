# type: ignore-all

import logging

from bs4 import BeautifulSoup
import requests

from quantiq.modules.scrapper.providers.fundamentus.data import StockDetails
from quantiq.modules.scrapper.providers.scrapper import Scrapper


class FundamentusScraper(Scrapper):
    def __init__(self):
        super().__init__("stocks")
        self.base_url = "https://www.fundamentus.com.br/detalhes.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.logger = logging.getLogger(__name__)

    def scrape(self, ticker: str) -> dict:
        try:
            self.logger.info(f"Scraping data for {ticker}")
            response = requests.get(
                f"{self.base_url}?papel={ticker}", headers=self.headers
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            if self._is_company_not_found(soup):
                raise Exception(
                    f"Company with ticker {ticker} not found on Fundamentus"
                )

            basic_info = self._table_rows_to_dict(
                self._extract_table_rows_by_header(soup, "Papel")
            )

            company_info = self._table_rows_to_dict(
                self._extract_table_rows_by_header(soup, "Valor de mercado")
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

            oscillations = self.oscillations_to_dict(
                self._extract_table_rows_by_header(soup, "Oscilações")
            )

            balance_sheet = self._table_rows_to_dict(
                self._extract_table_rows_by_header(soup, "Dados Balanço Patrimonial")
            )

            financial_results = self._parse_financial_results(
                self._extract_table_rows_by_header(
                    soup, "Dados demonstrativos de resultados"
                )
            )

            data = {
                **basic_info,
                **company_info,
                "last_financial_info": last_financial_info,
                "variations": oscillations.get("oscillations", {}),
                "indicators": oscillations.get("indicators", {}),
                "balance_sheet": balance_sheet,
                "financial_results": financial_results,
            }

            return StockDetails.create(data).model_dump()
            # return data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:  # type: ignore
                raise Exception(
                    f"Company with ticker {ticker} not found on Fundamentus"
                ) from e
            raise Exception(f"Failed to fetch data for {ticker}: {e!s}") from e
        except Exception as e:
            self.logger.error(f"Error scraping data for {ticker}: {e!s}")
            raise Exception(f"Failed to scrape data for {ticker}: {e!s}") from e

    def oscillations_to_dict(self, rows: list[list[str]]) -> dict:
        oscillations = {}
        indicators = {}
        for r in rows[1:12]:
            period = self._format_key(r[0])
            if period:
                oscillations[period] = self._parse_value(r[1])
            for i in range(2, len(r), 2):
                name = self._format_key(r[i])
                if name:
                    indicators[name] = self._parse_value(r[i + 1])

        return {
            "oscillations": oscillations,
            "indicators": indicators,
        }

    def _is_company_not_found(self, soup: BeautifulSoup) -> bool:
        error_message = soup.find("div", {"class": "error"})
        if error_message and "papel não encontrado" in error_message.text.lower():
            return True
        return False

    def _extract_table_as_rows(self, table: BeautifulSoup) -> list[list[str]]:
        rows_data = []
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all(["td", "th"])  # type: ignore
            cell_values = [col.get_text(strip=True) for col in cols]
            if cell_values:
                rows_data.append(cell_values)
        return rows_data

    def _table_rows_to_dict(self, rows: list[list[str]]) -> dict:
        result = {}
        for row in rows:
            if not row or len(row) < 2:
                continue

            for i in range(0, len(row) - 1, 2):
                key = self._format_key(row[i].strip())
                # TODO: remove this to data model
                if key == "ativo":
                    key = "ativos"

                if key == "patrim_liq":
                    key = "patrim_liquido"

                value = self._parse_value(row[i + 1].strip())
                if not key:
                    continue
                result[key] = value

        return result

    def _parse_financial_results(self, rows: list[list[str]]) -> dict:
        results = {"last_12_months": {}, "last_3_months": {}}
        for row in rows[2:]:
            label_12m = self._format_key(row[0].replace("?", "").strip())
            value_12m = self._parse_value(row[1].strip())
            label_3m = self._format_key(row[2].replace("?", "").strip())
            value_3m = self._parse_value(row[3].strip())
            if label_12m:
                results["last_12_months"][label_12m] = value_12m
            if label_3m:
                results["last_3_months"][label_3m] = value_3m
        return results
