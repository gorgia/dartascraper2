import logging
from datetime import datetime, date

from bs4 import BeautifulSoup
import re

from crawler.scraper.Scraper import Scraper
from dataobject.fund_data import FundData

log = logging.getLogger('dartascraper.FoundDataScaper')


def scrape_date(soup_page: BeautifulSoup) -> date:
    text = soup_page.find('span', class_=['last-update']).text
    text = text.replace('Dati aggiornati al ', '')
    return datetime.strptime(str(text), '%d/%m/%Y').date()


def scrape_ms_rate(soup_el: BeautifulSoup) -> date:
    text = soup_el.find('span', class_=['last-update']).text
    text = text.replace('Dati aggiornati al ', '')
    return datetime.strptime(str(text), '%d/%m/%Y').date()


def num_or_null(text: str):
    number_list = re.findall(r'\d+', text)
    if len(number_list) > 0:
        return int(number_list[0])
    else:
        return None


def float_or_null(text: str):
    if text is None or len(text) == 0 or 'n.d.' in text:
        return None
    text = text.strip('%').replace(',', '.')
    return float(text)


class AllianzDartaFundDataScraper(Scraper):
    def scrape_data(self, html):
        soup_page = BeautifulSoup(html, "lxml")
        tabella = soup_page.find('table', class_=['tabella'])
        last_update_date = scrape_date(soup_page)
        lines = tabella.find_all('tr')
        funds_data = []
        log.debug(f"the table has {len(lines)} lines of data")
        linecount = 0
        for line in lines:
            try:
                linecount = linecount + 1
                fund_data = FundData()
                fund_data.isin = line.find_next('td', attrs={'data-label': 'ISIN sottostante'}).text[0:12]
                if 'n.d.' in fund_data.isin or not len(fund_data.isin) > 0:
                    continue
                fund_data.date = last_update_date
                fund_data.managing_comp = line.find_next('td', attrs={'data-label': 'Brand Asset Manager'}).text
                fund_data.close = float_or_null(line.find_next('td', attrs={'data-label': 'Ultima quotazione'}).text)
                fund_data.managing_comm = float_or_null(
                    line.find_next('td', attrs={'data-label': 'Commissione di gestione'}).text)
                fund_data.typology = line.find_next('td', attrs={'data-label': 'Categorie'}).text
                fund_data.performance1d = float_or_null(line.find_next('td', attrs={'data-label': '%VAR'}).text)
                fund_data.rsi_index = num_or_null(line.find_next('td', attrs={'data-label': 'Indice RSI'}).text)
                fund_data.morning_star_rate = num_or_null(line.find_next('td', attrs={'data-label': lambda x: x and "Morningstar Rating" in x}).text)
                fund_data.morning_star_sust_rate = num_or_null(line.find_next('td', attrs={'data-label': lambda x: x and "Morningstar Sustainability" in x}).text)
                fund_data.performance_start_of_the_year = float_or_null(line.find_next('td', attrs={'data-label': 'Rendimenti YTD'}).text)
                fund_data.performance3y = float_or_null(line.find_next('td', attrs={'data-label': '3 anni - Ann.ti'}).text)
                fund_data.performance5y = float_or_null(line.find_next('td', attrs={'data-label': '5 anni - Ann.ti'}).text)
                fund_data.sharp_ratio = float_or_null(line.find_next('td', attrs={'data-label': 'Indice Sharpe'}).text)
                fund_data.year_volatility = float_or_null(line.find_next('td', attrs={'data-label': 'Volatilità'}).text)
                fund_data.site = 'allianzadartaie'
                funds_data.append(fund_data)
            except Exception as exception:
                log.error(f"Error occurred at line {linecount}")
                log.error(exception)
        return funds_data
