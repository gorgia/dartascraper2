from db import postgres_sql
import pytest
import logging

from crawler.AsyncCrawler import AsyncCrawler
from crawler.scraper.allianzdartaie.FundDataScraper import FundDataScraper

log = logging.getLogger(__name__)


def test_prova():
    log.info("Inizio test")
    url = 'https://news.allianzdarta.ie/darta-easy-selection/'
    crawler = AsyncCrawler(url, FundDataScraper(), enable_js=2)
    fund_datas = crawler.run()
    postgres_sql.save_funds(fund_datas)


test_prova()