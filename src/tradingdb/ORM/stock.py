from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
 

Base = declarative_base()
 
class Currency(Base):
    __tablename__ = 'currency'
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String,nullable=False, unique=True)
    
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column('id',Integer, nullable=True, primary_key=True)
    name = Column('name',String,nullable=False, unique=True)

class Stock(Base):
    __tablename__ = 'stock'
    id = Column('id',Integer, primary_key=True)
    symbol = Column('symbol',String,nullable=False, unique=True)
    yf_symbol = Column('yf_symbol',String,nullable=False, unique=True)  
    company = Column('company',String,nullable=False)
    exchange_id = Column('exchange_id',Integer,ForeignKey("exchange.id"),nullable=False) 
    currency_id = Column('currency_id',Integer,ForeignKey('currency.id'),nullable=False)
    exchange = relationship(Exchange,backref=backref('stocks'))
    

class Period(Base):
    __tablename__ = 'period'
    id = Column('id',Integer, primary_key=True)
    name = Column('name',String,nullable=False, unique=True)
    conversion_in_sec = Column('conversion_in_sec',Integer,nullable=False) 

class Price(Base):
    __tablename__ = 'stock_price'
    id = Column('id',Integer, primary_key=True)
    stock_id = Column('stock_id',Integer, ForeignKey("stock.id"))
    period_id = Column('period_id',Integer, ForeignKey("period.id"))
    date = Column('date', DateTime, nullable=False) 
    open = Column('open', Float, nullable= False)
    low = Column('low', Float, nullable= False)
    high = Column('high', Float, nullable= False)
    close = Column('close', Float, nullable= False)
    adjusted_close = Column('adjusted_close', Float, nullable= False)
    volume = Column('volume', Float, nullable= False)
    stock = relationship(Stock,
        backref=backref('prices',cascade='delete,all'))
    period = relationship(Period,
        backref=backref('prices'))
    __table_args__ = (UniqueConstraint('stock_id', 'period_id', 'date', 
                    name='unique_stock_date_period'),)
 
'''
from sqlalchemy import create_engine
engine = create_engine('sqlite:///stock_dats.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
'''