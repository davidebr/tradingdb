import argparse
import pandas as pd
from datetime import datetime

import sys
import os
import logging

import numpy as np
import pandas as pd
import shutil
import json
import urllib

from   datetime import datetime, timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError 
from sqlalchemy.orm.exc import NoResultFound

from matplotlib import pyplot as plt

from tradingdb.utils import *
from tradingdb.ORM.utils import *

def main():
    parser = argparse.ArgumentParser(description='Parse variables from command line.')
    parser.add_argument('--db', type=str, help='Path to the database file.')
    parser.add_argument('--interval', type=str, help='Interval value. e.g. 1h  ')
    parser.add_argument('--time_str', type=str, help='Time in the format "YYYY-MM-DD HH:mm:ss".')

    args = parser.parse_args()

    db_path = args.db
    interval = args.interval
    time_str = args.time_str

    # Print the parsed values
    print("db:", db_path)
    print("interval:", interval)
    print("time_str:", time_str)

    # If time_str is not provided, use the current time
    if not time_str:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert the time string to a datetime object
    try:
        datetime_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        print("Datetime object:", datetime_obj)
    except ValueError as e:
        print("Error: Invalid time string format. Please provide time in the format 'YYYY-MM-DD HH:mm:ss'.")



    DBNAME=os.path.abspath(db_path)
    session=get_new_session(DBNAME)

    def get_last_price_for_period(stock):
        period=[]
        date=[]
        for p in stock.prices:
            date.append(p.date)
            period.append(p.period.name)
        periods=set(period)
        df=pd.DataFrame({'date':date,'period':period})
        return {pp:df[df['period'] == pp]['date'].max().to_pydatetime() for pp in periods}


    stock_last_date={}
    with session.begin() as mysession:
        q=mysession.query(stock.Stock)
        #q=q.join(stock.Exchange)
        q=q.join(stock.Price)
        q=q.join(stock.Period)
        q=q.filter(stock.Period.name==interval)
        q=q.all()
        for r in q:
            stock_last_date[r.yf_symbol]=get_last_price_for_period(r)

    def add_dfd_to_yfsymbol(session,interval,dfd):
        with session.begin() as mysession:
            for k,df in dfd.items():
                nadd=0
                for index, row in df.iterrows():
                    # convert name into time
                    sid=mysession.query(stock.Stock.id).filter(stock.Stock.yf_symbol==k).one()[0]
                    pid=mysession.query(stock.Period.id).filter(stock.Period.name==interval).one()[0]
                    q=mysession.query(stock.Price)
                    q=q.filter(stock.Price.stock_id==sid)
                    q=q.filter(stock.Price.period_id==pid)
                    r=q.filter(stock.Price.date==index.to_pydatetime()).one_or_none()
                    if r is None:
                        #print("adding time ",index)
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
                        nadd+=1
                    #else:
                        #print("time ",index,"already in")
                print("Symbol ",k,": added ",nadd," timepoints for interval ",interval)

    for k,v in stock_last_date.items():
        time_end=datetime_obj    #v[interval]+timedelta(days=deltadays)
        time_start = v[interval]
        # fetch this
        dfd=download_data_from_yfsymbols(k,time_start,time_end,interval=interval)
        # add this
        add_dfd_to_yfsymbol(session,interval,dfd)
        #break

if __name__ == "__main__":
    main()
