from flask import Flask, render_template, request, jsonify, url_for
from mysqldb import connection
import datetime
import json


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("homepage.html")
        
@app.route('/sentiment_dashboard')
def sentiment_dashboard():
    return render_template("sentiment_dashboard.html")
    
@app.route('/sentiment_analysis/<sym>')
def sentiment_analysis(sym):
    c, conn = connection()    
    c.execute("SELECT * FROM stocks WHERE symbol = %s", (sym,))    
    data = c.fetchall()
    
    symbol = data[0][0]
    name = data[0][1]
    description = data[0][4]
    
    return render_template("sentiment_analysis.html", 
                           symbol=symbol, 
                           name=name,
                           description=description)
    
@app.route('/get_sentiment_sym/<sym>', methods=['GET', 'POST'])
def get_sentiment_sym(sym):
    c, conn = connection()
    c.execute("SELECT * FROM daily WHERE symbol = %s", (sym,))
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
#                                          
                             

@app.route('/get_dashboard_sentiment', methods=['GET', 'POST'])
def get_dashboard_sentiment():
    c, conn = connection()
    c.execute("SELECT * FROM dashboard")
    
    data = c.fetchall()
    
    symbol = []
    name = []
    industry = []
    sector = []
    sentiment = []
    sentiment_volume = []
    
    for i in data:          
        sent_data = c.fetchall()
        symbol.append(i[0])
        name.append(i[1])
        industry.append(i[2])
        sector.append(i[3])
        sentiment.append(i[4])
        sentiment_volume.append(i[5])
    
    return jsonify(result = [symbol,
                             name,
                             industry,
                             sector,
                             sentiment,
                             sentiment_volume])
                             
                             

        
        
        
    











                             
if __name__ == "__main__":
    app.run()