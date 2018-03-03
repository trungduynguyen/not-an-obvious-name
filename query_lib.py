# -*- coding: utf-8 -*-
"""
@author: Trung Duy
"""

DROP_QUERY = """DROP TABLE IF EXISTS {0};"""

CREATE_QUERY = """CREATE TABLE {0} ( date DATE PRIMARY KEY , 
                                     open FLOAT, 
                                     high FLOAT, 
                                     low FLOAT,
                                     close FLOAT NOT NULL, 
                                     volume FLOAT, 
                                     market_cap FLOAT);"""

WEEKLY_PRICE_QUERY = """select strftime('%Y-week(%W)',date) as year_week, AVG(close) weekly_average,
                               MAX(close) weekly_max,
                               MIN(close) weekly_min
                        from {0}
                        group by year_week;"""

MAX_RELATIVE_SPAN_QUERY = """select year_week ,MAX((weekly_max-weekly_min)/weekly_min) relative_span 
                             from (
                                    select strftime('%Y-week(%W)',date) as year_week,
                                           MAX(close) weekly_max,
                                           MIN(close) weekly_min
                                    from {0}
                                    group by year_week)"""