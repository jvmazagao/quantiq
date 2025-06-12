import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class FundamentusScraper:
    """Scraper for Fundamentus website."""
    
    def __init__(self):
        self.base_url = "https://www.fundamentus.com.br/detalhes.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape(self, ticker: str) -> Dict:
        """Scrape stock data from Fundamentus and return structured objects for each table."""
        try:
            logger.info(f"Scraping data for {ticker}")
            response = requests.get(f"{self.base_url}?papel={ticker}", headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if company exists
            if self._is_company_not_found(soup):
                raise Exception(f"Company with ticker {ticker} not found on Fundamentus")
            
            # Find all data tables
            tables = soup.find_all('table', {'class': 'w728'})
            if not tables:
                raise Exception(f"No data tables found for {ticker}")
            
            variations, indicators = self._parse_variations_and_indicators(self._extract_table_as_rows(tables[2]))
            # Parse and clean basic_info
            basic_info = self._parse_dict_values(self._clean_keys(self._table_rows_to_dict(self._extract_table_as_rows(tables[0]))))
            # Extract last_financial_info fields
            last_financial_keys = [
                "cotacao", "min_52_sem", "max_52_sem", "data_ult_cot", "vol_med_2m"
            ]
            last_financial_info = {k: basic_info.pop(k) for k in last_financial_keys if k in basic_info}
            data = {
                "basic_info": basic_info,
                "last_financial_info": last_financial_info,
                "market_values": self._parse_dict_values(self._clean_keys(self._table_rows_to_dict(self._extract_table_as_rows(tables[1])))),
                "variations": self._parse_dict_values(self._clean_keys(variations)),
                "indicators": self._parse_dict_values(self._clean_keys(indicators)),
                "balance_sheet": self._parse_dict_values(self._clean_keys(self._table_rows_to_dict(self._extract_table_as_rows(tables[3])))),
                "financial_results": self._clean_financial_results(self._parse_financial_results(self._extract_table_as_rows(tables[4])))
            }
            
            # Remove empty dicts from the result
            data = {k: v for k, v in data.items() if v}
            return data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception(f"Company with ticker {ticker} not found on Fundamentus")
            raise Exception(f"Failed to fetch data for {ticker}: {str(e)}")
        except Exception as e:
            logger.error(f"Error scraping data for {ticker}: {str(e)}")
            raise Exception(f"Failed to scrape data for {ticker}: {str(e)}")

    def _is_company_not_found(self, soup: BeautifulSoup) -> bool:
        """Check if the company was not found on Fundamentus."""
        error_message = soup.find('div', {'class': 'error'})
        if error_message and "papel não encontrado" in error_message.text.lower():
            return True
        return False

    def _extract_table_as_rows(self, table: BeautifulSoup) -> List[List[str]]:
        """Extract a table as a list of rows, each row is a list of cell values."""
        rows_data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cell_values = [col.get_text(strip=True) for col in cols]
            if cell_values:
                rows_data.append(cell_values)
        return rows_data

    def _table_rows_to_dict(self, rows: List[List[str]]) -> Dict:
        """Convert a table (list of rows) to a dictionary using each pair of columns as key-value."""
        result = {}
        for row in rows:
            # Process pairs: (key, value), (key, value), ...
            for i in range(0, len(row) - 1, 2):
                key = row[i].strip()
                value = row[i+1].strip()
                if key:
                    result[key] = value
        return result

    def _to_snake_case(self, s: str) -> str:
        """Convert a string to snake_case."""
        s = s.lower().replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c')
        s = re.sub(r'[^a-z0-9]+', '_', s)
        s = re.sub(r'_+', '_', s)
        return s.strip('_')

    def _clean_keys(self, d: Dict) -> Dict:
        """Remove leading '?' and extra spaces from all keys in a dict, and convert to snake_case."""
        return {self._to_snake_case(k.lstrip('?').strip()): v for k, v in d.items()}

    def _parse_value(self, value: str):
        """Parse a string value to int, float, percent, or ISO date if possible."""
        if value is None or value.strip() == '-':
            return None
            
        v = value.strip().replace('.', '').replace(' ', '')
        # Date detection (dd/mm/yyyy)
        date_match = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', value.strip())
        if date_match:
            try:
                dt = datetime.strptime(value.strip(), "%d/%m/%Y")
                return dt.strftime("%Y-%m-%dT00:00:00Z")
            except Exception:
                pass
        # Percentages
        if v.endswith('%'):
            try:
                return float(v[:-1].replace(',', '.'))
            except Exception:
                return value
        # Integers
        if v.isdigit():
            try:
                return int(v)
            except Exception:
                return value
        # Floats
        try:
            return float(v.replace(',', '.'))
        except Exception:
            # Return the original value for fields like nro_ac_es that should remain as strings
            return value

    def _parse_dict_values(self, d: Dict) -> Dict:
        """Parse all values in a dict using _parse_value."""
        return {k: self._parse_value(v) for k, v in d.items()}

    def _parse_variations_and_indicators(self, rows: List[List[str]]) -> (Dict, Dict):
        """Split the variations and indicators table into two dicts."""
        variations = {}
        indicators = {}
        for row in rows:
            # Skip header row if present
            if len(row) >= 4:
                # Left: variations (first two columns)
                var_key = row[0].strip()
                var_value = row[1].strip()
                if var_key and var_key not in ["Oscilações", ""]:
                    variations[var_key] = var_value
                # Right: indicators (next two columns)
                ind_key = row[2].replace('?', '').strip()
                ind_value = row[3].strip()
                if ind_key and ind_key not in ["Indicadores fundamentalistas", ""]:
                    indicators[ind_key] = ind_value
        return variations, indicators

    def _parse_financial_results(self, rows: List[List[str]]) -> Dict:
        """Parse the financial results table into last_12_months and last_3_months dicts."""
        results = {"last_12_months": {}, "last_3_months": {}}
        # Skip the header row (first row)
        for row in rows[1:]:
            if len(row) >= 4:
                label_12m = row[0].replace('?', '').strip()
                value_12m = row[1].strip()
                label_3m = row[2].replace('?', '').strip()
                value_3m = row[3].strip()
                if label_12m:
                    results["last_12_months"][label_12m] = self._parse_value(value_12m)
                if label_3m:
                    results["last_3_months"][label_3m] = self._parse_value(value_3m)
        return results

    def _clean_financial_results(self, results: dict) -> dict:
        """Clean and format the financial results as a nested object with snake_case keys and parsed values."""
        def to_snake_case(s):
            s = s.lower()
            s = s.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c')
            s = re.sub(r'[^a-z0-9]+', '_', s)
            s = re.sub(r'_+', '_', s)
            return s.strip('_')
        def parse_value(value):
            if value is None or value == '-' or value == '':
                return None
            v = str(value).strip().replace('.', '').replace(' ', '')
            if v.endswith('%'):
                try:
                    return float(v[:-1].replace(',', '.'))
                except Exception:
                    return value
            if v.isdigit():
                try:
                    return int(v)
                except Exception:
                    return value
            try:
                return float(v.replace(',', '.'))
            except Exception:
                return value
        return {
            'last_12_months': {to_snake_case(k): parse_value(v) for k, v in results.get('last_12_months', {}).items() if k.strip()},
            'last_3_months': {to_snake_case(k): parse_value(v) for k, v in results.get('last_3_months', {}).items() if k.strip()}
        }