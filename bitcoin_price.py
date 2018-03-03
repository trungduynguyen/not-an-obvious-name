# -*- coding: utf-8 -*-
"""
@author: Trung Duy NGUYEN
"""

import requests
import os
import sqlite3
import datetime as dt
import pandas as pd
import argparse
import logging

class BitcoinPrice:
    
    url = """https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={0}&market={1}&apikey={2}"""
    api_key = ""
    db_name = ""
    selected_cols = ['1b. open (USD)','2b. high (USD)','3b. low (USD)','4b. close (USD)','5. volume', '6. market cap (USD)']
    daily_df = pd.DataFrame()
    
    def __init__(self,api_key):
        
        self.api_key= api_key
        
    @staticmethod
    def read_from_csv(filename, columns):
        return pd.read_csv(filename,usecols=columns)
        
    def get_daily_df(self):
        self.daily_df = self.read_from_csv('./data/daily_data.csv',['close','year_week']) # Load from csv file
        self.daily_df['close'] = self.daily_df['close'].astype(float)
        logging.info("Extracted Date and close prices into Dataframe !")
    
    def get_digital_currency_daily(self,symbol= "BTC",market= "USD"):
        """ 
        Get bitcoin prices from alphavantage API and save to csv file
        """
        
        response= requests.get(self.url.format(symbol,market,self.api_key))
        
        json_response = response.json()
        logging.info("Collected daily data!")
        df = pd.DataFrame(json_response["Time Series (Digital Currency Daily)"]).T[self.selected_cols]
        df['Date'] = pd.to_datetime(df.index)   #Transform Date column to datetime datatype
        df.set_index('Date', inplace=True)
        df[df.columns] = df[df.columns].apply(pd.to_numeric)    #Convert prices to float
        df = df.resample('B').mean()                            # Filter and only get data in business day (from Mon to Fri)
        df.columns = ['open','high','low','close','volume','market_cap']    #Rename columns
        df['year_week'] = df.index.to_series().apply(lambda x: dt.datetime.strftime(x,'%Y-week(%U)'))   #Get week of the date
        
        df.to_csv('./data/daily_data.csv',sep=',')
        logging.info("Saved data to 'daily_data.csv' !")
        
        self.get_daily_df()
    
    def get_weekly_stats(self):
        pass
    
    def get_relative_span(self):
        pass


class BitcoinPricePandas(BitcoinPrice):
    
    def __init__(self,api_key):
        super().__init__(api_key)

    
    def get_weekly_stats(self):
        """
        Get weekly statistical measurements mean, max, min by pandas dataframe
        """
        print(self.daily_df.head())
        df_report = pd.DataFrame(index = self.daily_df['year_week'].unique() )
        df_report['weekly_average'] = (self.daily_df.groupby(['year_week']).mean())['close'] #Get average price in each week
        df_report['weekly_max'] = (self.daily_df.groupby(['year_week']).max())['close']  #Get maximum price in each week
        df_report['weekly_min'] = (self.daily_df.groupby(['year_week']).min())['close']  #Get minimum price in each week
        df_report.to_csv('./data/pandas_weekly_report.csv')
        logging.info("Save data to pandas_weekly_report.csv")
        return df_report
    
    @staticmethod
    def relative_span(self,x):
        """
        Apply mathematical formula to get weekly relative span
        """
        return (x['weekly_max'] - x['weekly_min']) / x['weekly_min']
    
    def get_max_relative_span(self,df_weekly):
        """
        Get maximum relative span by pandas dataframe
        """
        result = df_weekly.apply(self.relative_span,axis=1) #Apply relative_span for each row
        df_span = pd.DataFrame(dict(relative_span=result),index =df_weekly.index)
        print("Maximum relative span by Pandas Dataframe:\n")
        print(df_span[df_span['relative_span'] == df_span['relative_span'].max() ])  
    
    def process(self):
        
        weekly_df = self.get_weekly_stats()
        self.get_max_relative_span(weekly_df)
        



#    def create_table(self):
#        """
#        Create sqlite table and insert data from pandas DataFrame to table
#        """
#        
#        try:
#            conn = sqlite3.connect(self.db_name)
#            cur= conn.cursor()
#            cur.execute('''DROP TABLE IF EXISTS %s;'''%(self.table_name)) #Drop table if exists
#            
#            # Create new table and insert daily data
#            cur.execute('''CREATE TABLE %s ( date DATE PRIMARY KEY , 
#                                         open FLOAT, 
#                                         high FLOAT, 
#                                         low FLOAT,
#                                         close FLOAT NOT NULL, 
#                                         volume FLOAT, 
#                                         market_cap FLOAT,
#                                         year_week VARCHAR(15));'''%(self.table_name))
#            logging.info("Created the table!")
#    
#            daily_df = pd.read_csv('./data/daily_data.csv')
#            daily_df['Date'] = pd.to_datetime(daily_df['Date'])
#            daily_df.set_index('Date', inplace=True)
#            daily_df.to_sql(self.table_name,conn, if_exists='replace')
#            logging.info("Inserted the table!")
#            conn.commit()
#        except Exception as e:
#            logging.error("Error: ",e)
#        finally:
#            conn.close()
#    
#
#    def get_weekly_stats_query(self):
#        
#        conn = sqlite3.connect(self.db_name)
#        df = pd.read_sql_query('''select year_week, AVG(close) weekly_average,
#                                  MAX(close) weekly_max,
#                                  MIN(close) weekly_min
#                                  from %s
#                                  group by year_week'''%(self.table_name),conn)
#        df.to_csv('./data/sql_weekly_report.csv')
#        logging.info("Save data to sql_weekly_report.csv")
#        
#        return df
#        
#    def get_relative_span_query(self):
#        
#        conn = sqlite3.connect(self.db_name)
#        df = pd.read_sql_query('''select year_week ,MAX((weekly_max-weekly_min)/weekly_min) relative_span from (
#                                  select year_week,
#                                  MAX(close) weekly_max,
#                                  MIN(close) weekly_min
#                                     from %s
#                                     group by year_week)'''%(self.table_name), conn)
#        print(df)
#        return df
#        
#        
   
def main():
    
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('api_key', action="store", type=str)
    parser.add_argument('db_name', action="store", type=str)
    parser.add_argument('table_name', action="store", type=str)
    args = parser.parse_args()
    
    #logger = logging.getLogger(__name__)
    logging.info('Starting process')
    logging.basicConfig(level=logging.INFO)
    os.chdir(os.getcwd())
  
    #Inititate new instance
#    Bitcoin = BitcoinPrice(args.api_key)
    
    # Get Bitcoin daily prices via API and store to daily_data.csv file
#    Bitcoin.get_digital_currency_daily()
    
    btc_pandas = BitcoinPricePandas(args.api_key)
    
    btc_pandas.get_digital_currency_daily()
    
    print(btc_pandas.daily_df.head())
#  
#    # Create sqlite table to store data
#    Bitcoin.create_table()
  
#    #Compute method 1: Python Memory
#    weekly_df = Bitcoin.get_weekly_stats_pandas(daily_df)
#    Bitcoin.get_relative_span_pandas(weekly_df)
#  
#  
    #Compute method 2: SQL Queries
    #Bitcoin.get_weekly_stats_query() 
    #Bitcoin.get_relative_span_query()
#  
#    Bitcoin.close_db()
#  
#    print("FINISH PROGRAM!")

if __name__== "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)
    main()      

