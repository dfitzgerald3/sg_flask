from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from mysqldb import connection
import datetime
import json
import gc


app = Flask(__name__)


#Create Registration Form Class to be used during the registration process
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
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
@app.route('/registration')
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
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))

        
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