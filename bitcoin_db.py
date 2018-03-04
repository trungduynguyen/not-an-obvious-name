# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 14:51:42 2018

@author: Trung Duy
"""
import pandas as pd
import logging
import sqlite3
import query_lib as ql
from bitcoin_price import BitcoinPrice

class BitcoinPriceDB(BitcoinPrice):

    db_name = ""
    table_name = ""
    conn = None
    cursor = None
    
    def __init__(self, api_key, db_name, table_name):
        super().__init__(api_key)      
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.get_digital_currency_daily(save= False)
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
                      
    def query(self,query):
        
        try:
            df = pd.read_sql_query(query,self.conn)
        except Exception as e:
            logging.error(e)
        else:
            return df
    
    def create_table(self):
        """
        Create sqlite table and insert data from pandas DataFrame to table
        """
        try:    
            self.cursor.execute(ql.DROP_QUERY.format(self.table_name)) #Drop table if exist
            # Create new table and insert daily data
            self.cursor.execute(ql.CREATE_QUERY.format(self.table_name))
            daily_df = self.get_daily_df()

            daily_df.to_sql(self.table_name,self.conn, if_exists='replace')
            self.conn.commit()
            logging.info("Inserted into DB!")
        except Exception as e:
            logging.error(e)
        finally:
            self.cursor.close()
    

    def get_weekly_stats(self):
        
        df = self.query(ql.WEEKLY_PRICE_QUERY.format(self.table_name))
        df.set_index('year_week', inplace=True)
        df.to_csv('./data/sql_weekly_report.csv')
        logging.info("Saved weekly data to 'sql_weekly_report.csv' !")
        
        return df
        
    def get_max_relative_span(self):
        
        df = self.query(ql.MAX_RELATIVE_SPAN_QUERY.format(self.table_name))
        df.set_index('year_week', inplace=True)
        print("Maximum relative span by SQL query:\n",df)
        
        return df
    
    def process(self):
        
        self.create_table()
        weekly_df = self.get_weekly_stats()
        max_span = self.get_max_relative_span()