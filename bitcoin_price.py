# -*- coding: utf-8 -*-
"""
@author: Trung Duy NGUYEN
"""
import requests
import datetime as dt
import pandas as pd
import logging


URL = """https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={0}&market={1}&apikey={2}"""
SELECTED_COLS = ['1b. open (USD)','2b. high (USD)','3b. low (USD)','4b. close (USD)','5. volume', '6. market cap (USD)']
SAVED_COLS = ['open','high','low','close','volume','market_cap']

class BitcoinPrice:
    
    _api_key = ""
    _daily_df = pd.DataFrame()
    
    def __init__(self,api_key):
        
        self._api_key= api_key
        
    def set_daily_df(self,daily_df):
        self._daily_df = daily_df
        return self
        
    @staticmethod
    def read_from_csv(filename, columns):
        return pd.read_csv(filename, usecols=columns)
        
    def get_daily_df(self, columns = SAVED_COLS):
        
        self._daily_df['close'] = self._daily_df['close'].astype(float)
        logging.info("Extracted daily bitcoin prices !")
        return self._daily_df[columns]


    def get_digital_currency_daily(self, symbol= "BTC", market= "USD", save = True):
        """ 
        Get bitcoin prices from alphavantage API and save to csv file
        """
        
        response= requests.get(URL.format(symbol,market,self._api_key))
        
        json_response = response.json()
        logging.info("Collected daily data!")
        df = pd.DataFrame(json_response["Time Series (Digital Currency Daily)"]).T[SELECTED_COLS]
        df['Date'] = pd.to_datetime(df.index)   #Transform Date column to datetime datatype
        df.set_index('Date', inplace=True)
        df[df.columns] = df[df.columns].apply(pd.to_numeric)    #Convert prices to float
        df = df.resample('B').mean()                            # Filter and only get data in business day (from Mon to Fri)
        df.columns = self._saved_cols    #Rename columns
        df['year_week'] = df.index.to_series().apply(lambda x: dt.datetime.strftime(x,'%Y-week(%W)'))   #Get week of the date
        
        if(save):
            df.to_csv('./data/daily_data.csv', sep=',')
            logging.info("Saved data to 'daily_data.csv' !")
        self.set_daily_df(df)

    
    def get_weekly_stats(self):
        pass
    
    def get_max_relative_span(self):
        pass

    def process(self):
        pass


