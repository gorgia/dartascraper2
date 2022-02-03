import logging
from datetime import datetime

from bs4 import BeautifulSoup

from crawler.scraper.Scraper import Scraper
from dataobject.fund_data import FundData

log = logging.getLogger('dartascraper.FoundDataScaper')


def get_float_data(text, item_descr=None):
    try:
        value = float(str(text).strip('.').replace(',', '.').strip('%').strip('-'))
        if item_descr:
            log.debug(f"{item_descr} : {value}")
        return value
    except ValueError:
        log.debug("No value found for " + item_descr)


class FundDataScraper(Scraper):

    def __init__(self):
        self.soup_page = None

    def scrape_data(self, html):
        self.soup_page = BeautifulSoup(html, "lxml")
        fund_data = FundData()
        self.scrape_title(fund_data)
        self.scrape_descr(fund_data)
        self.scrape_img(fund_data)
        return fund_data

    def scrape_title(self, fund_data: FundData):
        title_el = self.soup_page.find('h1', class_=['c-head-title', 'big'])
        fund_data.title = str(title_el.text).replace("SCHEDA ", "").replace("Scheda ", "").strip('\n')

    def scrape_descr(self, fund_data: FundData):
        descrs = self.soup_page.find_all('li', class_='descr')  # self.webdriver.find_elements_by_class_name("descr")
        fund_data.close = get_float_data(descrs[0].text, "close")
        fund_data.var_perc = get_float_data(descrs[1].text, "var_perc")
        fund_data.managing_comp = str(descrs[2].text)
        fund_data.isin = str(descrs[3].text)
        if fund_data.isin: fund_data.isin = fund_data.isin.strip()
        fund_data.date = datetime.strptime(str(descrs[4].text), '%d/%m/%Y').date()
        fund_data.currency = str(descrs[5].text)
        fund_data.typology = str(descrs[6].text)
        log.debug(f"scraping isin: {fund_data.isin}")
        fund_data.performance1m = get_float_data(descrs[7].text, "performance1m")
        fund_data.performance6m = get_float_data(descrs[8].text, "performance6m")
        fund_data.performance1y = get_float_data(descrs[9].text, "performance1y")
        fund_data.performance_start_of_the_year = \
            get_float_data(descrs[10].text, "performance_start_of_the_year")
        fund_data.performance3y = get_float_data(descrs[11].text, "performance3y")
        fund_data.performance5y = get_float_data(descrs[12].text, "performance5y")

    def scrape_img(self, fund_data: FundData):
        image_el = self.soup_page.find('img', class_='c-chart-img')
        if image_el is not None:
            fund_data.graph_image_src = image_el.attrs['src']
