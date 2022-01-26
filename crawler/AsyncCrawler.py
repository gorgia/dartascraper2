from abc import ABC, abstractmethod

from singleton_decorator import singleton

from crawler.CrawlerBuilder import CrawlerBuilder
from crawler.SessionFactory import SessionFactory

@singleton
class AsyncCrawler(CrawlerBuilder):

    session = SessionFactory.get_async_session()
    

    def __init__(self) -> None:
        self.reset()

    def get_crawler(self) -> Crawler: