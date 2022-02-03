import concurrent.futures
import sys

from config import config
from crawler.AsyncCrawler import AsyncCrawler
from crawler.scraper.borseit.FundDataScraper import FundDataScraper
from dataobject.fund_data import FundData
from db import postgres_sql
from datetime import datetime
import logging


log = logging.getLogger('dartascraper.main')


def crawl_fund_data_url(url):
    crawler = AsyncCrawler(url, FundDataScraper())
    return crawler.run()


not_graceful = sys.argv[1:] and sys.argv[1] == '--not-graceful'


def main():
    logging.basicConfig(level=config['log_level'])
    log.info(f"Starting dartascraper {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    fund_data_list = []
    url_tuple_list = postgres_sql.get_all_urls_and_domains_tuple_list()
    log.info(f"Processing {len(url_tuple_list)} urls")
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_results = {executor.submit(crawl_fund_data_url, "https://"+urltuple[0]+urltuple[1]): FundData
                          for urltuple in url_tuple_list}
        for future in concurrent.futures.as_completed(future_results):
            fund_data = future.result()
            if fund_data:
                fund_data_list.append(fund_data)

    log.info(f"Found {len(fund_data_list)} funds data")
    postgres_sql.save_funds(fund_data_list)


if __name__ == '__main__':
    main()
