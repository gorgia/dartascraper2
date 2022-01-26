from abc import ABC, abstractmethod


class Scraper(ABC):

    @abstractmethod
    def scrape_data(self) -> None:
        pass

