from dataclasses import dataclass
from datetime import date

from sqlalchemy import Integer


@dataclass
class FundData(object):

    isin: str
    title: str
    graph_image_src: str
    performance1m: float
    performance6m: float
    performance_start_of_the_year: float
    performance1y: float
    performance3y: float
    performance5y: float
    date: date
    close: float
    var_perc: float
    currency: str
    typology: str
    managing_comp: str
    descr: str
    morning_star_rate: int
    morning_star_sust_rate: int
    rsi_index: int
    sharp_ratio: int
    year_volatility: int
    managing_comm: float



    #  def generate_id(self):
    #     date_to_be_used = self.date if self.date else date.today()
    #     return date_to_be_used.strftime('%s')+self.isin

    def to_dict(self):
        return {
            'title': self.title,
            'graph_image_src': self.graph_image_src,
            'performance1m': self.performance1m,
            'performance6m': self.performance6m,
            'performance_start_of_the_year': self.performance_start_of_the_year,
            'performance1y': self.performance1y,
            'performance3y': self.performance3y,
            'performance5y': self.performance5y,
            'date': self.date,
            'close': self.close,
            'var_perc': self.var_perc,
            'isin': self.isin,
            'currency': self.currency,
            'typology': self.typology,
            'managing_comp': self.managing_comp
        }