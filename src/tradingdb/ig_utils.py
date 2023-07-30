import logging
import json
import sys
from trading_ig import IGService
from trading_ig.config import config
import logging

log = logging.getLogger(__name__)

class ig_session:
  def __init__(self):
      self.ig_service = IGService(config.username, config.password, config.api_key, config.acc_type)
      self.ig_service.create_session()
  def last_spread(self,epic):
      resolution='1Min'
      num_points=200
      response = self.ig_service.fetch_historical_prices_by_epic_and_num_points(epic, resolution, num_points) 
      bid_open=response['prices']['bid']['Open']
      ask_open=response['prices']['ask']['Open']
      mean_val=ask_open.subtract(bid_open).dropna().mean()
      max_val=ask_open.subtract(bid_open).dropna().max()
      min_val=ask_open.subtract(bid_open).dropna().min()
      mean_perc=ask_open.subtract(bid_open).div(ask_open).dropna().mean()*100
      max_perc=ask_open.subtract(bid_open).div(ask_open).dropna().max()*100
      min_perc=ask_open.subtract(bid_open).div(ask_open).dropna().min()*100
      return {'spread_avg':mean_val,'spread_min':min_val,'spread_max':max_val,
             'spreadperc_avg':mean_perc,'spreadperc_min':min_perc,'spreadperc_max':max_perc}
  def get_epic(self,symbol):
      return self.ig_service.search_markets(symbol)
if __name__=="__main__":
   logging.basicConfig(level=logging.DEBUG)
   sess=ig_session()
   print(sess.get_epic('VOD'))
   d=sess.last_spread("KA.D.VOD.DAILY.IP") 
   print(d) 
   print(sess.get_epic('VDTK'))
   d=sess.last_spread("KC.D.VDTKLN.DAILY.IP") 
   print(d) 
 
 
