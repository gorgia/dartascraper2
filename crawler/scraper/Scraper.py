from abc import abstractmethod


class Scraper:

    @abstractmethod
    def scrape_data(self, html) -> object:
        pass
