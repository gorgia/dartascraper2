from requests_html import HTMLSession
from scraper.Scraper import Scraper
import logging

log = logging.getLogger('dartascraper.AsyncCrawler')


class AsyncCrawler:

    def __init__(self, url, scraper: Scraper):
        super().__init__()
        self.session = HTMLSession()
        self.scraper = scraper
        self.url = url

    def run(self) -> object:
        log.debug("Getting page:" + self.url)
        result = self.session.get(self.url)
        html = result.html.html
        return self.scraper.scrape_data(html)



