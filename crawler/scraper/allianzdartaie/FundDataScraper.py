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


class FundDataScraper(Scraper):

    def scrape_data(self, html):
        soup_page = BeautifulSoup(html, "lxml")
        tabella = soup_page.find('table', class_=['tabella'])
        last_update_date = scrape_date(soup_page)
        linee = tabella.find_all('tr')
        funds_data = []
        for linea in linee:
            fund_data = FundData()
            fund_data.date = last_update_date
            fund_data.isin = linea.find_next('td', attrs={'data-label': 'ISIN sottostante'}).text
            fund_data.managing_comp = linea.find_next('td', attrs={'data-label': 'Brand Asset Manager'}).text
            fund_data.close = float(linea.find_next('td', attrs={'data-label': 'Ultima quotazione'}).text)
            fund_data.managing_comm = float(linea.find_next('td', attrs={'data-label': 'Commissione di gestione'}).text.strip('%'))
            fund_data.performance1d = float(linea.find_next('td', attrs={'data-label': '%VAR'}).text.strip('%'))
            fund_data.rsi_index = num_or_null(linea.find_next('td', attrs={'data-label': 'Indice RSI'}).text)
            fund_data.morning_star_rate = num_or_null(linea.find_next('td', attrs=
            {'data-label': lambda x: x and "Morningstar Rating" in x}).text)
            fund_data.morning_star_sust_rate = num_or_null(linea.find_next('td', attrs=
            {'data-label': lambda x: x and "Morningstar Sustainability" in x}).text)
            fund_data.performance_start_of_the_year = linea.find_next('td', attrs={'data-label': 'Rendimenti YTD'}).text
            fund_data.performance3y = linea.find_next('td', attrs={'data-label': '3 anni - Ann.ti'}).text
            fund_data.performance5y = linea.find_next('td', attrs={'data-label': '5 anni - Ann.ti'}).text
            fund_data.sharp_ratio = linea.find_next('td', attrs={'data-label': 'Indice Sharpe'}).text
            fund_data.year_volatility = linea.find_next('td', attrs={'data-label': 'Volatilità'}).text
            funds_data.append(fund_data)
        return funds_data

