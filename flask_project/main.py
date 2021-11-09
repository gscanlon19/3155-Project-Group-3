# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask
from flask import render_template# Flask is the web app that we will cust

app = Flask(__name__)  #create an app

@app.route('/login')
def login():
    return render_template('login.html')

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)),debug=True)
