from sqlalchemy import create_engine, Float, Date
from sqlalchemy.orm import join, sessionmaker
from sqlalchemy import Table, MetaData, Column, String, ForeignKey

metadata = MetaData(schema="borsait")

found_table = Table('found', metadata,
                    Column('isin', String, primary_key=True),
                    Column('title', String),
                    Column('descr', String),
                    Column('managing_comp', String),
                    Column('currency', String)
                    )

data_table = Table('data', metadata,
                   Column('isin_id', String, ForeignKey('found.isin'), primary_key=True),
                   Column('performance1m', Float),
                   Column('performance6m', Float),
                   Column('performance_start_of_the_year', Float),
                   Column('performance1y', Float),
                   Column('performance3y', Float),
                   Column('performance5y', Float),
                   Column('date', Date, primary_key=True),
                   Column('var_perc', Float),
                   Column('currency', String),
                   Column('typology', String),
                   Column('managing_comp', String)
                   )

found_date_join = join(found_table, data_table)

engine = create_engine(
    'postgresql://andrea:Luglio1985!@localhost:5432/database1-instance-1.c56crgps8bcg.eu-south-1.rds.amazonaws.com')


def save(found_data_list):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(found_data_list)
    session.commit()
    session.close()
