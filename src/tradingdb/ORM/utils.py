import os,sys,pathlib

from requests import session
from . import stock
import logging
import subprocess

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError 

from ..settings import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(format)
logger.addHandler(handler)

VALID_INTERVALS={   '1m':60,
                        '2m':2*60,
                        '5m':5*60,
                        '15m':15*60,
                        '30m':30*60,
                        '60m':60*60,
                        '90m':90*60,
                        '1h':60*60,
                        '1d':24*60*60,
                        '5d':5*24*60*60,
                        '1wk':7*24*60*60,
                        '1mo':30*24*60*60,
                        '3mo':90*24*60*60,
                        }

def get_new_session(dbpath):
    engine = create_engine('sqlite:///'+dbpath)
    session = sessionmaker()
    session.configure(bind=engine)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    return session
           
def initialize_db(dbpath,overwrite=False):

        if not os.path.isfile(dbpath) or overwrite:
            mydir=pathlib.Path(stock.__file__).resolve().parent
            script=os.path.join(mydir,'database.sql')
            logger.debug("Sql script: "+script)
            ps1 = subprocess.run(['cat',script], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ps2 = subprocess.run(['sqlite3',dbpath], universal_newlines=True, input=ps1.stdout, stderr=subprocess.PIPE, stdout=subprocess.PIPE)  
            #print(ps1.stdout,ps2.stderr)
            session=get_new_session(dbpath)
            add_intervals(session)
            add_currencies(session)
            add_exchanges(session)
            
            return True
        else:
            return False

def add_currencies(session):
    for c in CURRENCIES:
        newcurrency=stock.Currency(name=c)
        with session.begin() as mysession:
            mysession.add(newcurrency)

def add_exchanges(session):
    with session.begin() as mysession:
        for name,v in EXCHANGES.items():
            newexchange=stock.Exchange(name=name)
            mysession.add(newexchange)



def add_intervals(session):

        with session.begin() as mysession:
              for k in VALID_INTERVALS.keys():
                   #logger.debug("Adding "+k+" interval")
                   p=stock.Period(name=k,conversion_in_sec=VALID_INTERVALS[k])
                   mysession.add(p)
              #mysession.commit()
        #logger.debug("Intervals addition done")


def add_df_to_yfsymbol(session,symbol,df,interval,commit=False):
    """add a dataframe to the database using yfsymbol as key

    Args:
        session (session): the sqlalchemy session
        symbol (str): string for yf_symbol in orm
        df (pandas.DataFrame): pandas daraframe
        interval (str): the interval of the data, e.g. 1d, 1h, 1m

    """

    # get stock id
    with session.begin() as mysession:
            for index, row in df.iterrows():
                # convert name into time
                sid=mysession.query(stock.Stock.id).filter(stock.Stock.yf_symbol==symbol).one()[0]
                pid=mysession.query(stock.Period.id).filter(stock.Period.name==interval).one()[0]
                #print(index)
                q=mysession.query(stock.Price)
                q=q.filter(stock.Price.stock_id==sid)
                q=q.filter(stock.Price.period_id==pid)
                r=q.filter(stock.Price.date==index.to_pydatetime()).one_or_none()
                if r is None:
                    p=stock.Price(
                                stock_id=sid,
                                period_id=pid,
                                date=index.to_pydatetime(),  
                                open=row['Open'],
                                low=row['Low'],
                                high=row['High'],
                                close=row['Close'],
                                adjusted_close=row['Adj Close'],
                                volume=row['Volume'])
                    mysession.add(p)
            if commit is False: session.rollback()
