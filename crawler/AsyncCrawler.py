from requests_html import HTMLSession
import logging
from collections.abc import Iterable
import html

from crawler.scraper import Scraper

log = logging.getLogger('dartascraper.AsyncCrawler')


class AsyncCrawler:

    def __init__(self, url, scraper: Scraper, enable_js=0):
        super().__init__()
        self.session = HTMLSession()
        self.scraper = scraper
        self.url = url
        self.enable_js = enable_js

    def run(self, javascript=5) -> Iterable:
        log.debug("Getting page:" + self.url)
        r = self.session.get(self.url)
        if self.enable_js > 0:
            r.html.render(sleep=self.enable_js)
        html = r.html.html
        return self.scraper.scrape_data(html)



