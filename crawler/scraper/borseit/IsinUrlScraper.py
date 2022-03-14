from bs4 import BeautifulSoup
import logging

from crawler.scraper.Scraper import Scraper

log = logging.getLogger('pyselscraper.isinscraper')


class IsinUrlScraper(Scraper):

    def scrape_data(self, html):
        if html:
            soup_page: BeautifulSoup = BeautifulSoup(html, 'lxml')
        else:
            log.error("Cannot scrape anything: HTML is empty")
            return
        main_el = soup_page.find('div', class_="main")
        c_container = main_el.find('div', class_="c-container__inner")
        if c_container is None:
            raise Exception("c-container is none. thats a problem")
        if "Nessun titolo trovato" in c_container.text:
            log.info("ISIN NOT FOUND")
            return
        else:
            ccell_element = soup_page.find("div", id=lambda x: x and "descrizione_donotchange" in x)
            #ccell_element = soup_page.find("div", {"id": self.isin})
            a_element = ccell_element.find('a', href=True)
            href = a_element["href"]
            log.info("isin found! url is:\n" + href)
            return href
