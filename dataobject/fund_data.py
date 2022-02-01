from dataclasses import dataclass
from datetime import date
from sqlalchemy.orm import column_property
from db.db_schema import found_table, found_date_join, data_table


@dataclass
class FundData(object):
    __table__ = found_date_join
    id = column_property(found_table.c.isin, data_table.c.isin_id)
    isin_id = found_table.c.isin

    isin: str = '' #field(default_factory='')
    title: str = ''
    graph_image_src: str = '' #field(default_factory='')
    performance1m: float = -100.0 #field(default_factory=0.0)
    performance6m: float = -100.0 #field(default_factory=0.0)
    performance_start_of_the_year: float = -100.0 #field(default_factory=0.0)
    performance1y: float = -100.0 #field(default_factory=0.0)
    performance3y: float = -100.0 #field(default_factory=0.0)
    performance5y: float = -100.0 #field(default_factory=0.0)
    date: date = date.today() #field(default_factory=date(1970, 1, 1))
    close: float = -100.0 #field(default_factory=0.0)
    var_perc: float = -100.0 #field(default_factory=0.0)
    currency: str = '' #field(default_factory='')
    typology: str = '' #field(default_factory='')
    managing_comp: str = '' #field(default_factory='')
    descr: str = ''

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



