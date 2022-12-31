import unittest
import sys
import os
import logging
import numpy as np
import argparse
import copy
import pandas as pd
import shutil
import subprocess

from datetime import datetime, timedelta


import tradingdb

from tradingdb.ORM import utils
from tradingdb.ORM import stock 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError 

BOGUS_CUR='boguscur'
BOGUS_XC='bogusxc'
BOGUS_ST='bogusst'

OFFLINE=True


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# since unittest reassign the stderr/stdout you need to re-specify the handler here
# https://stackoverflow.com/questions/7472863/pydev-unittesting-how-to-capture-text-logged-to-a-logging-logger-in-captured-o
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

TEST_DB='test.db'
TRADINGDB_PATH = os.path.dirname(tradingdb.__file__) 
TEST_DB_PATH=os.path.join(TRADINGDB_PATH,"../","../","tests",TEST_DB)

class TestStockORM(unittest.TestCase):

    def setUp(self):
        #logger.debug("\nSetting up now...")
        if not os.path.isfile(TEST_DB):
          # execute the script         
          # sqlite3 test.sqlt <  database.sql 
          script=os.path.join(TRADINGDB_PATH,'ORM','database.sql')
          ps1 = subprocess.run(['cat',script], 
               universal_newlines=True, 
               stdout=subprocess.PIPE, 
               stderr=subprocess.PIPE)
          ps2 = subprocess.run(['sqlite3',TEST_DB_PATH], 
               universal_newlines=True, 
               input=ps1.stdout, 
               stderr=subprocess.PIPE, 
               stdout=subprocess.PIPE)
          #logger.debug("SQL: "+ps1.stdout)
          #logger.debug("SQLITE errors "+ps2.stderr)
          #logger.debug("Running tests from: "+os.getcwd())
        else:
          logger.debug("Database already existing!")

        engine = create_engine('sqlite:///'+TEST_DB_PATH)
        self.session = sessionmaker()
        self.session.configure(bind=engine)
        self.Base = declarative_base()
        self.Base.metadata.create_all(engine)
        utils.add_intervals(self.session)
           
    def tearDown(self):
          #logger.debug("tear down instance")
          try:
               delete_bogus_stock()
          except:
               pass
          try:
               delete_bogus_exchange()
          except:
               pass
          try:
               delete_bogus_currency()
          except: 
               pass
          if os.path.isfile(TEST_DB_PATH):
               os.remove(TEST_DB_PATH) 


    def create_bogus_currency(self):
            newcurrency=stock.Currency(name=BOGUS_CUR)
            with self.session.begin() as mysession:
                 mysession.add(newcurrency)
    
    def delete_bogus_currency(self):
            with self.session.begin() as mysession:
                 ret=mysession.query(stock.Currency).filter(stock.Currency.name==BOGUS_CUR).one()
                 mysession.delete(ret)
                 mysession.commit()
    
    def create_bogus_exchange(self):
            with self.session.begin() as mysession:
                 newexchange=stock.Exchange(name=BOGUS_XC)
                 mysession.add(newexchange)
                 mysession.commit()
    
    def delete_bogus_exchange(self):
            # now remove the fake currency
            with self.session.begin() as mysession:
                 ret=mysession.query(stock.Exchange).filter(stock.Exchange.name==BOGUS_XC).one()
                 mysession.delete(ret)
                 mysession.commit()
    
    def create_bogus_stock(self):
            with self.session.begin() as mysession:
                 eid=mysession.query(stock.Exchange.id).filter(stock.Exchange.name==BOGUS_XC).one()[0]
                 cid=mysession.query(stock.Currency.id).filter(stock.Currency.name==BOGUS_CUR).one()[0]

                 newstock=stock.Stock(company=BOGUS_ST,symbol=BOGUS_ST,
                         yf_symbol=BOGUS_ST,exchange_id=eid,currency_id=cid)

                 mysession.add(newstock)
                 mysession.commit()
    
    def delete_bogus_stock(self):
            # now remove the fake currency
            with self.session.begin() as mysession:
                 ret=mysession.query(stock.Stock).filter(stock.Stock.company=='bogusst').one()
                 mysession.delete(ret)
                 mysession.commit()
         
    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    def add_data_to_symbol(self,symbol,df,interval):
         valid_intervals='1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo'.split(',')
         #get stock id first
    
         #add_intervals()
         if interval not in valid_intervals:
              raise ValueError('interval '+interval+'not in '+','.join(valid_intervals)) 
         try:
              with self.session.begin() as mysession:
                   sid=mysession.query(stock.Stock.id).filter(stock.Stock.symbol==symbol).one()[0]
                   pid=mysession.query(stock.Period.id).filter(stock.Period.name==interval).one()[0]
    
                   for index, row in df.iterrows():
                        # convert name into time
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
    
                   mysession.commit()
                   #print(row)
              return True
         except: 
              raise
     
    def test_dummy(self):
        self.assertEqual('hello','hello')

    def test_create_currency(self):

        newcurrency=stock.Currency(name=BOGUS_CUR)

        with self.session.begin() as mysession:
             mysession.add(newcurrency)
             mysession.commit()
             # now I try to add it again and should trigger an error
             with self.assertRaises(InvalidRequestError):
                mysession.add(newcurrency)

        # now remove the fake currency
        with self.session.begin() as mysession:
             ret=mysession.query(stock.Currency).filter(stock.Currency.name==BOGUS_CUR).one()
             mysession.delete(ret)
             mysession.commit()


    def test_create_exchange(self):

        # create a new currency
        newcurrency=stock.Currency(name=BOGUS_CUR)
        with self.session.begin() as mysession:
             mysession.add(newcurrency)
             # implicitely called with session.close(): mysession.commit()

        with self.session.begin() as mysession:
             newexchange=stock.Exchange(name=BOGUS_XC)
             mysession.add(newexchange)
             mysession.commit()
             # now I try to add it again and should trigger an error
             with self.assertRaises(InvalidRequestError):
                mysession.add(newexchange)

        # now remove the fake currency
        with self.session.begin() as mysession:
             ret=mysession.query(stock.Currency).filter(stock.Currency.name==BOGUS_CUR).one()
             mysession.delete(ret)
             ret=mysession.query(stock.Exchange).filter(stock.Exchange.name==BOGUS_XC).one()
             mysession.delete(ret)

    def test_create_exchange(self):

 
        with self.session.begin() as mysession:
          
             newexchange=stock.Exchange(name=BOGUS_XC)
             mysession.add(newexchange)
             mysession.commit()
             # now I try to add it again and should trigger an error
             with self.assertRaises(InvalidRequestError):
                mysession.add(newexchange)

        # now remove the fake currency
        with self.session.begin() as mysession:
             ret=mysession.query(stock.Exchange).filter(stock.Exchange.name==BOGUS_XC).one()
             mysession.delete(ret)

    def test_create_exchange2(self):

        self.create_bogus_exchange()

        with self.session.begin() as mysession:
             newexchange=stock.Exchange(name=BOGUS_XC)
             # now I try to add it again and should trigger an error
             with self.assertRaises(IntegrityError):
                mysession.add(newexchange)
                mysession.commit()

        self.delete_bogus_exchange()

    def test_create_stock(self):

        self.create_bogus_currency()
        self.create_bogus_exchange()
        self.create_bogus_stock()

        with self.session.begin() as mysession:
             eid=mysession.query(stock.Exchange.id).filter(stock.Exchange.name==BOGUS_XC).one()[0]
             cid=mysession.query(stock.Currency.id).filter(stock.Currency.name==BOGUS_CUR).one()[0]

             newstock=stock.Stock(company=BOGUS_ST,symbol=BOGUS_ST,exchange_id=eid,currency_id=cid)
             # now I try to add it again and should trigger an error
             with self.assertRaises(IntegrityError):
                mysession.add(newstock)
                mysession.commit()

        self.delete_bogus_stock()
        self.delete_bogus_exchange()
        self.delete_bogus_currency()

    #    #symbols=finance_tools.download_ftse_symbols('FTSE-100')
    #def test_symbols_ftse100(self):

    def test_symbol_download_vod(self):
        deltadays=10
        myend=datetime.today()
        time_end = myend   + timedelta(days=1)
        time_start = myend - timedelta(days=deltadays)

        if OFFLINE:
          mypath=os.path.join(TRADINGDB_PATH,'../../','data','VOD.L.csv')
          logger.debug(" ... Offline data loading from csv...")
          df={'VOD.L':pd.read_csv(mypath,index_col=0,parse_dates=[0])}
        else:
          df=finance_tools.download_data_from_symbols(['VOD'],time_start,time_end,interval='1d',mypath=None)
          self.assertTrue(len(df['VOD.L'])>0)

        # now create fake currencty and exchange
        self.create_bogus_currency()
        self.create_bogus_exchange()
        self.create_bogus_stock()

        self.assertTrue(self.add_data_to_symbol(BOGUS_ST,df['VOD.L'],'1d'))

        self.delete_bogus_stock() 
        self.delete_bogus_exchange()
        self.delete_bogus_currency()

if __name__=='__main__':
     #parser = argparse.ArgumentParser(description='ORM testing')
     #parser.add_argument('--offline', action='store_true')

     #args = parser.parse_args(copy.deepcopy(sys.argv))
     #print(args.offline)
     unittest.main()
#