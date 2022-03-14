import typing

from requests_html import HTMLSession
import logging

from crawler.scraper import Scraper

log = logging.getLogger('dartascraper.AsyncCrawler')


class AtomicSyncCrawler:

    def __init__(self, url, scraper: Scraper, enable_js=False):
        super().__init__()
        self.scraper = scraper
        self.url = url
        self.enable_js = enable_js

    def run(self) -> typing.Any:
        log.debug("Getting page:" + self.url)
        cycle_count = 0
        htmltext = ''
        while not htmltext and cycle_count < 3:
            try:
                with HTMLSession() as s:
                    with s.get(self.url) as r:
                        if self.enable_js:
                            r.html.render(sleep=2, timeout=120)
                        htmltext = r.html.html
            except Exception as e:
                log.warning(str(e))
            finally:
                cycle_count = cycle_count+1
        if not htmltext:
            return None
        return self.scraper.scrape_data(htmltext)



