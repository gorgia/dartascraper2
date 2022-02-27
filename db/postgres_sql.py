import datetime

import pandas as pd
import psycopg2
import logging

from dataobject.fund_data import FundData
from config import config

log = logging.getLogger('dartascraper.sql')


def get_db_connection():
    return psycopg2.connect(host=config['sql']['server_url'], dbname=config['sql']['dbname'],
                            user=config['sql']['user'], password=config['sql']['password'],
                            options=config['sql']['options'])


def save_fund(fund):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur1:
                upsert_fund(fund, cur1)
    except Exception as e:
        log.exception(e)


def save_funds(fund_data_list):
    log.debug(f"Saving {len(fund_data_list)} funds")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur1:
                for fund in fund_data_list:
                    upsert_fund(fund, cur1)
            with conn.cursor() as cur2:
                for fund in fund_data_list:
                    upsert_fund_data(fund, cur2)
            conn.commit()
    except Exception as e:
        log.exception(e)


def get_new_isin():
    with get_db_connection() as conn:
        with conn.cursor() as cr:
            sql = "SELECT isin FROM borsait.fund f WHERE  NOT EXISTS ( " \
                  "SELECT FROM   borsait.fund_url WHERE  isin = f.isin)"
            cr.execute(sql)
            tmp = cr.fetchall()
            return tmp


def upsert_fund(fund: FundData, cursor):
    sql = """INSERT INTO fund as f(isin, title, descr, managing_comp, currency,typology, ms_star, ms_sust, managing_comm)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (isin)
                DO UPDATE
                set ms_star = coalesce(excluded.ms_star,  f.ms_star),
                    ms_sust = coalesce(excluded.ms_sust,  f.ms_sust),
                    managing_comm = coalesce(excluded.managing_comm,  f.managing_comm),
                    typology = coalesce(excluded.typology,  f.typology)
                    """
    cursor.execute(sql, (fund.isin, fund.title, fund.descr, fund.managing_comp, fund.currency,
                         fund.typology, fund.morning_star_rate, fund.morning_star_sust_rate, fund.managing_comm))


def upsert_fund_data(fund: FundData, cursor):
    sql = """INSERT INTO fund_quote
                (isin_id, date, performance1m, performance6m, performance_start_of_the_year,
                 performance1y, performance3y, performance5y, close, performance1d, 
                  sharp_ratio, rsi, year_volatility,  site)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (isin_id, date)
                DO NOTHING"""
    cursor.execute(sql, (fund.isin, fund.date, fund.performance1m,
                         fund.performance6m, fund.performance_start_of_the_year,
                         fund.performance1y, fund.performance3y, fund.performance5y, fund.close, fund.performance1d,
                         fund.sharp_ratio, fund.rsi_index, fund.year_volatility, fund.site))


def upsert_found_data_url(isin: str, url: str, domain: str, last_update: datetime.date, cursor):
    sql = """INSERT INTO fund_url
                (isin, url, domain, last_update
                VALUES(%s, %s, %s, %s)
                ON CONFLICT (isin, last_update)
                DO NOTHING"""
    cursor.execute(sql, (isin, url, domain, last_update))


def get_all_urls_and_domains_tuple_list():
    with get_db_connection() as conn:
        with conn.cursor() as cr:
            sql = """SELECT * FROM borsait.fund_url
                    ORDER BY isin ASC, domain ASC """
            cr.execute(sql)
            tmp = cr.fetchall()

    # Extract the column names
    col_names = []
    for elt in cr.description:
        col_names.append(elt[0])

    # Create the dataframe, passing in the list of col_names extracted from the description
    df = pd.DataFrame(tmp, columns=col_names)
    domain_url_df = df[['domain', 'url']]
    return list(domain_url_df.itertuples(index=False, name=None))