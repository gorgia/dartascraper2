from requests_html import HTMLSession
import logging

from crawler.scraper import Scraper

log = logging.getLogger('dartascraper.AsyncCrawler')


class AsyncCrawler:

    def __init__(self, url, scraper: Scraper, enable_js=0):
        super().__init__()
        self.session = HTMLSession()
        self.scraper = scraper
        self.url = url
        self.enable_js = enable_js

    def run(self, javascript=5) -> object:
        log.debug("Getting page:" + self.url)
        result = self.session.get(self.url)
        if self.enable_js > 0:
            result.html.render(sleep=self.enable_js)
        html = result.html.html
        return self.scraper.scrape_data(html)



