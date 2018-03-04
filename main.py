# -*- coding: utf-8 -*-
"""
@author: Trung Duy
"""

import argparse
import logging
from bitcoin_pandas import BitcoinPricePandas as bitpd
from bitcoin_db import BitcoinPriceDB as bitdb
import pathlib

PATHS = ['./data','./db']

def main(api_key,db_name,table_name):
       
    logging.info('Starting process')
  
    #Inititate new instance
    btc_pandas = bitpd(api_key)
    
    # Get Bitcoin daily prices via API and store to daily_data.csv file 
    btc_pandas.process()
  
    # Create sqlite table to store data
    with bitdb(api_key,db_name,table_name) as btc_db:
        btc_db.process()

if __name__== "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('api_key', action="store", type=str)
    parser.add_argument('db_name', action="store", type=str)
    parser.add_argument('table_name', action="store", type=str)
    args = parser.parse_args()
    
    for path in PATHS:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    
    main(args.api_key, args.db_name, args.table_name)      
