# -*- coding: utf-8 -*-
"""
@author: Trung Duy
"""
import sys
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from bitcoin_pandas import BitcoinPricePandas as bitpd
from bitcoin_db import BitcoinPriceDB as bitdb

class TestBitcoin(unittest.TestCase):
    
    API_KEY = ""
    DB_NAME = ""
    TABLE_NAME = ""
    
    def test_weekly_data(self): 
        """
        Test if two weekly_data csv files from both pandas and sql are equal
        """
    
        try:
            pd_df = pd.read_csv('./data/pandas_weekly_report.csv')
            db_df = pd.read_csv('./data/sql_weekly_report.csv')  
        except Exception as e:
            raise Exception(e)
        
        assert_frame_equal(pd_df.astype(str), db_df.astype(str), check_dtype=False, check_names=False)
        
        
    def test_max_relative_span(self):
        """
        Test if two maximum weekly relative span values from both pandas and sql are equal
        """
        try:
            btc_pandas = bitpd(self.API_KEY)
            pd_df = btc_pandas.read_from_csv('./data/pandas_weekly_report.csv')
            pd_df.set_index('year_week',inplace = True)
            pd_max_span = btc_pandas.get_max_relative_span(pd_df)
            
            btc_db = bitdb(self.API_KEY, self.DB_NAME, self.TABLE_NAME)
            db_max_span = btc_db.get_max_relative_span()
        except Exception as e:
            raise Exception(e)
        
        assert_frame_equal(pd_max_span.astype(str), db_max_span.astype(str), check_dtype=False, check_names=False)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
       TestBitcoin.TABLE_NAME = sys.argv.pop()
       TestBitcoin.DB_NAME = sys.argv.pop()
       TestBitcoin.API_KEY = sys.argv.pop()
       
    unittest.main(exit=False)