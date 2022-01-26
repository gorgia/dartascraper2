from abc import ABC

from singleton_decorator import singleton

from crawler.Crawler import Crawler


@singleton
class CrawlerBuilder(ABC):

    def get_crawler(self) -> None:
        pass

    def set_crawler_session(self) -> None:
        pass

    def set_page_parser(self) -> None:
        pass


