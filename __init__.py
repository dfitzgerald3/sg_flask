from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify, make_response
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from mysqldb import connection
import datetime
import json
import gc
import pandas as pd
from functools import wraps



app = Flask(__name__)


#Create Registration Form Class to be used during the registration process
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=150)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])


#Render HOMEPAGE
@app.route('/')
def homepage():
    return render_template("homepage.html")
    

#Render ABOUT 
@app.route('/about')
def about():
    return render_template("about.html")
    
    
#Render PRODUCTS
@app.route('/products')
def products():
    return render_template("products.html")
    

#Render REGISTRATION
@app.route('/registration', methods=["GET", "POST"])
def registration():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                status = "Fail"
                return render_template('register.html', form=form, status=status)
                
            elif str(form.password.data) != str(form.confirm.data):
                flash("Passwords must match!")
                status = "Fail"
                return render_template('register.html', form=form, status=status)

            else:
                c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email)))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('sentiment_dashboard'))
        
        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))




#Create LOGIN REQUIRED decorator
#Used to limit access to certain pages
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap
    
    
    
#Render LOGIN
@app.route('/login', methods = ["GET", "POST"])
def login():
    error = ''
    
    try:
        if request.method == "POST":
            c, conn = connection()
            
            c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            
            data = c.fetchone()
            
            if data is None:
                error = "Invalid credentials, try again."
                
            else:
                if sha256_crypt.verify(request.form['password'], data[2]):
                    session['logged_in'] = True
                    session['username'] = request.form['username']
        
                    flash("You are now logged in")
                    return redirect(url_for("sentiment_dashboard"))
    
                else:
                    error = "Invalid credentials, try again."
    
        gc.collect()
    
        return render_template("login.html", error=error)
        
    except Exception as e:
        return str(e)



#Render DASHBOARD
@app.route('/sentiment_dashboard')
@login_required
def sentiment_dashboard():
    return render_template("sentiment_dashboard.html")
    
    
    
#Render SENTIMENT ANALYSIS   
@app.route('/sentiment_analysis/<sym>')
@login_required
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
                           
                           
                           
#Retrieve SENTIMENT DATA
@app.route('/get_sentiment_sym/<sym>', methods=['GET', 'POST'])
@login_required
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
                             
                             
                             

#Retrieve DASHBOARD SENTIMENT
@app.route('/get_dashboard_sentiment', methods=['GET', 'POST'])
@login_required
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
                             
                             

#Function to DOWNLOAD DASHBOARD SENTIMENT
@app.route("/download_dashboard", methods = ["GET"])
def download_dashboard():
    c, conn = connection()
    c.execute("SELECT * FROM dashboard")
    data = c.fetchall()
    
    df = pd.DataFrame(list(data))
    columns = ['Symbol', 'Security Name', 'Sector', 'Industry', 'Recent Sentiment', 'Sentiment Volume']
    df.columns = columns
    
    csv = df.to_csv()
    
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-type"] = "text/csv"

    return response            
        
        
#Function to DOWNLOAD SECURITY SENTIMENT
@app.route("/download_sentiment/<sym>", methods = ["GET"])
def download_sentiment(sym):
    c, conn = connection()        
    c.execute("SELECT * FROM hourly WHERE symbol = %s", (sym.lower(),))
    data = c.fetchall()
    
    df = pd.DataFrame(list(data))
    
    columns = ['Date', 'Symbol', 'Sentiment', 'Volume']
    
    df.columns = columns
    
    symbol = df['Symbol'].iloc[0]
    
    df = df.drop('Symbol', 1)
    
    df['Date'] = pd.to_datetime(df['Date'], unit = 's')
    
    csv = df.to_csv()
    
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=" + symbol + ".csv"
    response.headers["Content-type"] = "text/csv"

    return response  
















#Create LOGOUT 
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))
    
    











                             
if __name__ == "__main__":
    app.run()