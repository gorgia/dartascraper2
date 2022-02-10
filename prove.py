import collections

import pytest

from crawler.AsyncCrawler import AsyncCrawler
from crawler.scraper.allianzdartaie.FundDataScraper import FundDataScraper


def test_prova():
    url = 'https://news.allianzdarta.ie/darta-easy-selection/'
    crawler = AsyncCrawler(url, FundDataScraper(), enable_js=2)
    fund_datas = crawler.run()
    if fund_datas is collections.Iterable:
        for fund_data in fund_datas:
            print(fund_data)
