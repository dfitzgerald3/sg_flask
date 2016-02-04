#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from mysqldb import connection
import datetime
import pandas as pd

#Retrieve sentiment data from database and put it in a pandas dataframe format
def retrieve_sentiment(sym):
    sym = str(sym)
        
    c, conn = connection()
        
    c.execute("SELECT * FROM sentiment WHERE symbol = %s", (sym,))
    
    data = c.fetchall()
    
    symbol = []
    sentiment = []
    time = []
    
    for i in data:
        symbol.append(i[0])
        sentiment.append(i[1])
#        time.append(datetime.datetime.fromtimestamp(int(i[2])).strftime('%Y-%m-%d %H:%M'))
        time.append(datetime.datetime.fromtimestamp(int(i[2])))
    
    df = pd.DataFrame(symbol)
    df['sentiment'] = sentiment
    df['time'] = time
    
    return df
    

#Function designed to bin data based on defined frequency
def sentiment_bin(df, freq):
    
    if freq == 'day':
        trans = lambda x: x.day
    elif freq == 'month':
        trans = lambda x: x.month
    
    
    day = df.time.apply(trans)
    
    df['day'] = day
    
    mean = df.groupby('day').mean()
    
    sentiment_mean = list(mean.sentiment.values)
    index = list(mean.index.values)
    
    return sentiment_mean, index
    