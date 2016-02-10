from flask import Flask, render_template, request, jsonify
from mysqldb import connection
import datetime
import retrieve_sentiment as rs

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")
        
@app.route('/sentiment_dashboard')
def sentiment_dashboard():
    return render_template("sentiment_dashboard.html")
    
@app.route('/test')
def test():
    return render_template("stringfilter.html")
    

@app.route('/get_sentiment', methods=['GET', 'POST'])
def get_sentiment():
    c, conn = connection()
    c.execute("SELECT * FROM daily WHERE symbol = 'xom'")
    data = c.fetchall()
    
    year = []
    month = []
    day = []
    stock_open = []
    stock_close = []
    stock_high = []
    stock_low = []
    sent = []
    sent_volume = []
    
    sent = []
    
    for i in data:
        date = datetime.datetime.fromtimestamp(i[0])        
        year.append(date.year)
        month.append(date.month)
        day.append(date.day)
        stock_open.append(i[2])
        stock_close.append(i[3])
        stock_high.append(i[4])
        stock_low.append(i[5])        
        sent.append(i[6])
        sent_volume.append(i[7])
        
    return jsonify(result = [year, 
                             month, 
                             day, 
                             stock_open, 
                             stock_close, 
                             stock_high, 
                             stock_low, 
                             sent, 
                             sent_volume])
                             
                             
@app.route('/get_dashboard_sentiment', methods=['GET', 'POST'])
def get_sentimen_sentimentt():
    c, conn = connection()
    c.execute("SELECT * FROM stocks")
    
    data = c.fetchall()
    
    symbol = []
    name = []
    industry = []
    sector = []
    sentiment = []
    sentiment_volume = []
    
    for i in data:
        try:
            c.execute("SELECT sentiment, volume FROM hourly WHERE time = (SELECT MAX(time) FROM hourly) AND symbol = %s", (i[0], ))        
            sent_data = c.fetchall()
            sentiment.append(sent_data[0][0])
            sentiment_volume.append(sent_data[0][1])
            symbol.append(i[0])
            name.append(i[1])
            industry.append(i[2])
            sector.append(i[3])        
            
        except Exception:
            continue
        
    return jsonify(result = [symbol,
                             name,
                             industry,
                             sector,
                             sentiment,
                             sentiment_volume])
        
        
        
        
    











                             
if __name__ == "__main__":
    app.run()