# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask
from flask import render_template # Flask is the web app that we will cust
from flask import redirect, url_for
from database import db
from models import Post as Post

app = Flask(__name__)  #create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

#login
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

#registration
@app.route('/registration')
def registration():
    return render_template('registration.html')

#Posts
@app.route('/posts')
def get_posts():

    my_posts = db.session.query(Post).all()

    return render_template('posts.htm', posts=my_posts)



app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)),debug=True)
