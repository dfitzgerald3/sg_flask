from flask import Flask, render_template
from mysqldb import connection
import datetime
import retrieve_sentiment as rs

app = Flask(__name__)


@app.route('/')
def homepage():
    c, conn = connection()
    
    c.execute("SELECT * FROM sentiment WHERE symbol = 'xom'")
    
    data = c.fetchall()
    
    sentiment = []
    
    for i in data:
        array = []
        array.append(i[0])
        array.append(i[1])
        array.append(datetime.datetime.fromtimestamp(int(i[2])).strftime('%Y-%m-%d %H:%M'))
        
        sentiment.append(array)
        
#    return jsonify(str(sent))
    return render_template("main.html", 
                           sentiment=sentiment)
#    return render_template("main.html")
                           
                           
@app.route('/test')
def test():
    df = rs.retrieve_sentiment('xom')
    s, i = rs.sentiment_bin(df, 'day')
    
    tally = len(s)
    
    return render_template('test.html', s=s, i=i, tally=tally)
    

if __name__ == "__main__":
    app.run()