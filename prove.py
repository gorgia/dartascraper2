from crawler.scraper.borseit.IsinUrlScraper import IsinUrlScraper
from db import postgres_sql
import logging

from crawler.AtomicSyncCrawler import AtomicSyncCrawler
from crawler.scraper.allianzdartaie.AllianzDartaFundDataScraper import AllianzDartaFundDataScraper

log = logging.getLogger(__name__)


def test_prova():
    log.info("Inizio test")
    url = 'https://news.allianzdarta.ie/darta-easy-selection/'
    crawler = AtomicSyncCrawler(url, AllianzDartaFundDataScraper(), enable_js=2)
    fund_datas = crawler.run()
    postgres_sql.save_funds(fund_datas)


def test_update_borseit_urls():
    newisins = postgres_sql.get_new_isin()
    fund_data_urls = []
    for isin_tuple in newisins:
        isin = isin_tuple[0]
        url = "https://www.borse.it/quotazioni/ricerca/?isin=" + isin + "&cerca_per=isin"
        crawler = AtomicSyncCrawler(url, IsinUrlScraper(), enable_js=0)
        fund_data_url = crawler.run()
        fund_data_urls.append(fund_data_url)
    log.info(f"fund data url is: {fund_data_urls}")


test_update_borseit_urls()