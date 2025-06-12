import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import logging
import re
from datetime import datetime

class FundamentusREITScraper:
    """Scraper para FIIs/REITs do Fundamentus (refatorado)."""
    def __init__(self):
        self.base_url = "https://www.fundamentus.com.br/detalhes.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _to_snake_case(self, s):
        s = s.lower()
        s = s.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c')
        s = re.sub(r'[^a-z0-9]+', '_', s)
        s = re.sub(r'_+', '_', s)
        return s.strip('_')

    def _parse_value(self, value):
        if value is None or value.strip() == '-':
            return None
        v = value.strip().replace('.', '').replace(' ', '')
        # Percentual
        if v.endswith('%'):
            try:
                return float(v[:-1].replace(',', '.'))
            except Exception:
                return value
        # Inteiro
        if v.isdigit():
            try:
                return int(v)
            except Exception:
                return value
        # Float
        try:
            return float(v.replace(',', '.'))
        except Exception:
            return value

    def _extract_basic_info(self, soup):
        """Extrai a tabela principal de informações básicas e cotação."""
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')
        basic_info = {}
        cotacao_info = {}
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) == 4:
                k1, v1, k2, v2 = [c.get_text(strip=True) for c in cols]
                k1 = self._to_snake_case(k1.lstrip('?').strip())
                k2 = self._to_snake_case(k2.lstrip('?').strip())
                if k1:
                    basic_info[k1] = self._parse_value(v1)
                if k2 in ["cotacao", "data_ult_cot", "min_52_sem", "max_52_sem", "vol_med_2m"]:
                    cotacao_info[k2] = self._parse_value(v2)
            elif len(cols) == 2:
                k, v = [c.get_text(strip=True) for c in cols]
                k = self._to_snake_case(k.lstrip('?').strip())
                if k in ["cotacao", "data_ult_cot", "min_52_sem", "max_52_sem", "vol_med_2m"]:
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
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and 'Oscilações' in header.get_text():
                rows = table.find_all('tr')[1:]  # pula o cabeçalho
                oscilations = {}
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2:
                        k = self._to_snake_case(cols[0].get_text(strip=True).lstrip('?').strip())
                        v = self._parse_value(cols[1].get_text(strip=True))
                        if k:
                            oscilations[k] = v
                return oscilations
        return {}

    def _extract_indicadores(self, soup):
        """Extrai os indicadores (lado direito da tabela Indicadores) de forma simples."""
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and 'Indicadores' in header.get_text():
                indicadores = {}
                for tr in table.find_all('tr'):
                    cells = [cell.get_text(strip=True) for cell in tr.find_all(['th', 'td'])]
                    if len(cells) >= 4:
                        key = cells[2]
                        val = cells[3]
                        # Limpa e converte a chave
                        key = key.lower().replace('.', '').replace('/', '_').replace(' ', '_')
                        try:
                            val = float(val.replace('.', '').replace(',', '.').replace('%', ''))
                        except Exception:
                            pass
                        indicadores[key] = val
                return indicadores
        return {}

    def _extract_table_rows_by_header(self, soup, header_text):
        """Returns all rows (array of arrays) from the table whose header contains header_text."""
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and header_text in header.get_text():
                rows = []
                for tr in table.find_all('tr'):
                    cells = [cell.get_text(strip=True) for cell in tr.find_all(['th', 'td'])]
                    if cells:
                        rows.append(cells)
                return rows
        return []

    def row_to_dict(self, rows):
        d = {}
        for r in rows:
            for i in range(0, len(r) - 1, 2):
                k = self._to_snake_case(r[i])
                v = self._parse_value(r[i+1])
                if k and v is not None:
                    d[k] = v
        return d

    def oscillations_to_dict(self, rows):
        oscillations = {}
        indicators = {}
        for r in rows[1:4]:
            period = self._to_snake_case(r[0])
            oscillations[period] = self._parse_value(r[1])
            for i in range(2, len(r), 2):
                name = self._to_snake_case(r[i].lstrip('?').strip())
                val  = self._parse_value(r[i+1])
                indicators[name] = val

        raw = rows[4]
        for i, cell in enumerate(raw):
            if cell == '12 meses' or re.match(r'^\d{4}$', cell):
                period = self._to_snake_case(cell)
                oscillations[period] = self._parse_value(raw[i+1])

        metrics_rows = [
            r for r in rows[5:]
            if len(r) >= 6 and r[0] and r[2].startswith('?')
        ]
        m12 = {}
        m3  = {}
        for r in metrics_rows:
            name   = self._to_snake_case(r[2])
            val12  = self._parse_value(r[3])
            val3   = self._parse_value(r[5])
            m12[name] = val12
            m3[name]  = val3
        indicators_by_period = {
            'last_12_months': m12,
            'last_3_months':  m3
        }

        # Balance Sheet: everything after the marker
        # find the row that contains 'Balanço Patrimonial'
        bs_idx = next(i for i, r in enumerate(rows) if 'Balanço Patrimonial' in r)
        this_row = rows[bs_idx]
        pos = this_row.index('Balanço Patrimonial')
        part1 = this_row[pos+1:]
        flat = [x for x in (part1) if x]
        bs_data = { self._to_snake_case(flat[i]): self._parse_value(flat[i+1]) for i in range(0, len(flat), 2) }

        return {
            'oscillations':         oscillations,
            'indicators':           indicators,
            'indicators_by_period': indicators_by_period,
            'balance_sheet':        bs_data
        }

    def scrape(self, ticker: str) -> dict:
        """Extracts all main sections as arrays of row arrays and returns basic_info_dict from the first row."""
        logger.info(f"Scraping REIT data for {ticker}")
        response = requests.get(f"{self.base_url}?papel={ticker}", headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        if self._is_reit_not_found(soup):
            raise Exception(f"REIT with ticker {ticker} not found on Fundamentus")
        basic_info_dict = self.row_to_dict(self._extract_table_rows_by_header(soup, "FII"))
        oscillations_dict = self.oscillations_to_dict(self._extract_table_rows_by_header(soup, "Oscilações"))
        properties_dict = self.row_to_dict(self._extract_table_rows_by_header(soup, "Imóveis"))
        
        return {
            **oscillations_dict,
            "company": basic_info_dict,
            "properties": properties_dict
        }

    def _is_reit_not_found(self, soup: BeautifulSoup) -> bool:
        """Check if the REIT was not found on Fundamentus."""
        error_message = soup.find('div', {'class': 'error'})
        if error_message and "papel não encontrado" in error_message.text.lower():
            return True
        return False

    def _extract_imoveis_table(self, soup: BeautifulSoup) -> dict:
        """Extract the 'Imóveis' table as a dictionary."""
        # Find the table with the header 'Imóveis'
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and 'Imóveis' in header.get_text():
                rows = table.find_all('tr')[1:]
                imoveis_data = {}
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) == 6:
                        imoveis_data[cols[0].get_text(strip=True)] = cols[1].get_text(strip=True)
                        imoveis_data[cols[2].get_text(strip=True)] = cols[3].get_text(strip=True)
                        imoveis_data[cols[4].get_text(strip=True)] = cols[5].get_text(strip=True)
                return imoveis_data
        return {}

    def _clean_imoveis_info(self, raw_dict):
        def to_snake_case(s):
            s = s.lower()
            s = s.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c')
            s = re.sub(r'[^a-z0-9]+', '_', s)
            s = re.sub(r'_+', '_', s)
            return s.strip('_')
        def parse_value(value):
            if value is None or value.strip() == '-':
                return None
            v = value.strip().replace('.', '').replace(' ', '')
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
                return value
        return {
            to_snake_case(k.lstrip('?').strip()): parse_value(v)
            for k, v in raw_dict.items()
            if k.strip() and v.strip()
        }

    def _extract_balance_sheet_table(self, soup: BeautifulSoup) -> dict:
        """Extract the 'Balanço Patrimonial' table as a dictionary for REITs."""
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and 'Balanço Patrimonial' in header.get_text():
                rows = table.find_all('tr')[1:]
                balance_data = {}
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) == 2:
                        balance_data[cols[0].get_text(strip=True)] = cols[1].get_text(strip=True)
                return balance_data
        return {}

    def _extract_all_resultados_tables(self, soup: BeautifulSoup):
        """Extract all 'Resultados' or 'Results' tables as a list of dicts."""
        resultados_tables = []
        for table in soup.find_all('table'):
            header = table.find('tr')
            if header and (('Resultados' in header.get_text()) or ('Results' in header.get_text())):
                rows = table.find_all('tr')[1:]
                # Try to parse as a two-period table (12m/3m)
                if rows and len(rows[0].find_all(['td', 'th'])) >= 4:
                    last_12_months = {}
                    last_3_months = {}
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 4:
                            k12 = cols[0].get_text(strip=True)
                            v12 = cols[1].get_text(strip=True)
                            k3 = cols[2].get_text(strip=True)
                            v3 = cols[3].get_text(strip=True)
                            if k12:
                                last_12_months[k12] = v12
                            if k3:
                                last_3_months[k3] = v3
                    resultados_tables.append({
                        'last_12_months': last_12_months,
                        'last_3_months': last_3_months
                    })
                else:
                    # Fallback: parse as a simple key-value table
                    result = {}
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 2:
                            k = cols[0].get_text(strip=True)
                            v = cols[1].get_text(strip=True)
                            if k:
                                result[k] = v
                    resultados_tables.append(result)
        return resultados_tables

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

