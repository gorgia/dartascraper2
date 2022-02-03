import pytest

from crawler.AsyncCrawler import AsyncCrawler
from crawler.scraper.allianzdartaie.FundDataScraper import FundDataScraper


def test_prova():
    url = 'https://news.allianzdarta.ie/darta-easy-selection/'
    crawler = AsyncCrawler(url, FundDataScraper(), enable_js=2)
    crawler.run()

