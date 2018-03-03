# -*- coding: utf-8 -*-
"""
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

weekly_price_query = """select strftime('%Y-week(%W)',date) as year_week, AVG(close) weekly_average,
                               MAX(close) weekly_max,
                               MIN(close) weekly_min
                        from {0}
                        group by year_week;"""

max_relative_span_query = """select year_week ,MAX((weekly_max-weekly_min)/weekly_min) relative_span 
                            from (
                                    select strftime('%Y-week(%W)',date) as year_week,
                                           MAX(close) weekly_max,
                                           MIN(close) weekly_min
                                    from {0}
                                    group by year_week)"""