# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 22:19:40 2018

@author: Trung Duy
"""

drop_query = """DROP TABLE IF EXISTS {0};"""

create_query = """CREATE TABLE {0} ( date DATE PRIMARY KEY , 
                                     open FLOAT, 
                                     high FLOAT, 
                                     low FLOAT,
                                     close FLOAT NOT NULL, 
                                     volume FLOAT, 
                                     market_cap FLOAT);"""

weekly_price_query = """"""

max_relative_span_query = """"""