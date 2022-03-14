import concurrent.futures
import sys
from collections.abc import Iterable
from config import config
from crawler.AtomicSyncCrawler import AtomicSyncCrawler
from crawler.scraper.borseit.IsinUrlScraper import IsinUrlScraper
from dataobject.fund_data import FundData
from db import postgres_sql
from datetime import datetime
from crawler.scraper.allianzdartaie.AllianzDartaFundDataScraper import AllianzDartaFundDataScraper
from crawler.scraper.borseit.BorseitFundDataScraper import BorseitFundDataScraper
import logging

logging.basicConfig(level=config['log_level'])
log = logging.getLogger('dartascraper.main')



not_graceful = sys.argv[1:] and sys.argv[1] == '--not-graceful'


def crawl_borseit() -> Iterable:
    log.info("start crawling borse.it")
    fund_data_list = []
    url_tuple_list = postgres_sql.get_all_urls_and_domains_tuple_list()
    log.info(f"Processing {len(url_tuple_list)} urls")
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_results = {executor.submit(AtomicSyncCrawler("https://" + urltuple[0] + urltuple[1], BorseitFundDataScraper(),
                                                            enable_js=3).run): FundData
                          for urltuple in url_tuple_list}
        for future in concurrent.futures.as_completed(future_results):
            fund_data = future.result()
            if fund_data:
                fund_data_list.append(fund_data)
    log.info(f"Found {len(fund_data_list)} funds data in borse.it")
    return fund_data_list


def crawl_allianzdartaie() -> Iterable:
    url = 'https://news.allianzdarta.ie/darta-easy-selection/'
    crawler = AtomicSyncCrawler(url, AllianzDartaFundDataScraper(), enable_js=True)
    allianzdartaie_fund_datas = crawler.run()
    return allianzdartaie_fund_datas


def update_borseit_urls():
    newisins = postgres_sql.get_new_isin()
    fund_data_urls = []
    for isin in newisins:
        url = "https://www.borse.it/quotazioni/ricerca/?isin=" + isin + "&cerca_per=isin"
        crawler = AtomicSyncCrawler(url, IsinUrlScraper(), enable_js=0)
        fund_data_url = crawler.run()
        if fund_data_url is None:
            log.info(f"Url for {isin} not found on borseit.")
        else:
            log.info(f"Url for {isin} is {fund_data_url}")
            postgres_sql.upsert_found_data_url(isin=isin, url=fund_data_url, domain="borseit")
    return fund_data_urls


def main():
    logging.basicConfig(level=config['log_level'])
    log.info(f"Starting dartascraper {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    allianzdartaie_funds_data = crawl_allianzdartaie()
    postgres_sql.save_funds(allianzdartaie_funds_data)
    update_borseit_urls()
    borseit_funds_data = crawl_borseit()
    postgres_sql.save_funds(borseit_funds_data)



if __name__ == '__main__':
    main()
