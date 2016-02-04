#Function designed to bin data based on defined frequency

def sentiment_bin(df, freq):
    trans = lambda x: x.freq
    
    day = df.time.apply(trans)
    
    df['day'] = day
    
    mean = df.groupby('day').mean()
    
    sentiment_mean = list(mean.sentiment.values)
    index = list(mean.index.values)
    
    return sentiment_mean, index