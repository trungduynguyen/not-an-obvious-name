# -*- coding: utf-8 -*-
"""

@author: Trung Duy
"""

import pandas as pd
import logging
from bitcoin_price import BitcoinPrice

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
    def relative_span(x):
        """
        Apply mathematical formula to get weekly relative span
        """
        return (x['weekly_max'] - x['weekly_min']) / x['weekly_min']
    
    def get_max_relative_span(self,df_weekly):
        """
        Get maximum relative span by pandas dataframe
        """
        print(df_weekly.head())
        result = df_weekly.apply(self.relative_span,axis=1) #Apply relative_span for each row
        df_span = pd.DataFrame(dict(relative_span=result),index =df_weekly.index)
        print("Maximum relative span by Pandas Dataframe:")
        print(df_span[df_span['relative_span'] == df_span['relative_span'].max() ])  
    
    def process(self):
        
        weekly_df = self.get_weekly_stats()
        self.get_max_relative_span(weekly_df)
        