# -*- coding: utf-8 -*-
"""

@author: Trung Duy
"""

import argparse
import logging
from bitcoin_pandas import BitcoinPricePandas

def main(api_key,db_name,table_name):
       
    logging.info('Starting process')
  
    #Inititate new instance
    btc_pandas = BitcoinPricePandas(api_key)
    
    # Get Bitcoin daily prices via API and store to daily_data.csv file 
    btc_pandas.get_digital_currency_daily()
    btc_pandas.process()
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
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('api_key', action="store", type=str)
    parser.add_argument('db_name', action="store", type=str)
    parser.add_argument('table_name', action="store", type=str)
    args = parser.parse_args()
    
    main(args.api_key,args.db_name,args.table_name)      
