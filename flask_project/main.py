# imports
import os  
import bcrypt
from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
from database import db
from models import Post as Post, User
from forms import RegisterForm
from flask import session
from forms import LoginForm
from models import Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        all_posts = db.session.query(Post)

        return render_template("index.html", user=session['user'], posts=all_posts)

    return render_template("index.html")


@app.route('/filters', methods=['POST', 'GET'])
def filters():
    if session.get('user'):

        if request.method == 'POST':

            sort = request.form.get("sort")

            if sort == "first_name":

                all_posts = db.session.query(Post).order_by('first_name')

            elif sort == "title":

                all_posts = db.session.query(Post).order_by('title')

            elif sort == "date":

                all_posts = db.session.query(Post).order_by('date')

            else:

                all_posts = db.session.query(Post).order_by('first_name')

            return render_template("index.html", user=session['user'], posts=all_posts)

    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():

        the_user = db.session.query(User).filter_by(email=request.form['email']).one()

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):

            session['user'] = the_user.first_name
            session['user_id'] = the_user.id

            return redirect(url_for('get_posts'))

        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:

        return render_template("login.html", form=login_form)


# Posts
@app.route('/posts')
def get_posts():
    if session.get('user'):

        my_posts = db.session.query(Post).filter_by(user_id=session['user_id']).all()

        return render_template('posts.html', posts=my_posts, user=session['user'])

    else:

        return redirect(url_for('login'))


# Post
@app.route('/posts/<post_id>')
def get_post(post_id):
    if session.get('user'):

        my_post = db.session.query(Post).filter_by(id=post_id).one()

        form = CommentForm()

        return render_template('post.html', post=my_post, form=form)
    else:
        return redirect(url_for('login'))


# new posts
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['postText']
            image = request.form['image']
            first_name = session['user']
            likes = 0
            dislikes = 0
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Post(title, text, image, today, session['user_id'], first_name, likes, dislikes)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_posts'))


        else:
            return render_template('newPost.html', user=session['user'])

    else:
        return redirect(url_for('login'))


# edit Post
@app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['postText']
            image = request.form['image']
            post = db.session.query(Post).filter_by(id=post_id).one()

            post.title = title
            post.text = text
            post.image = image
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('get_posts'))
        else:
            my_post = db.session.query(Post).filter_by(id=post_id).one()
            return render_template('newPost.html', post=my_post, user=session['user'])
    else:
        return redirect(url_for('login'))


# delete Post
@app.route('/posts/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    if session.get('user'):
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        db.session.delete(my_post)
        db.session.commit()

        return redirect(url_for('get_posts'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():

        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())

        first_name = request.form['firstname']
        last_name = request.form['lastname']

        new_user = User(first_name, last_name, request.form['email'], h_password)

        db.session.add(new_user)
        db.session.commit()

        session['user'] = first_name
        session['user_id'] = new_user.id

        return redirect(url_for('get_posts'))

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():

    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/posts/<post_id>/comment', methods=['POST'])
def new_comment(post_id):
    if session.get('user'):
        comment_form = CommentForm()

        if comment_form.validate_on_submit():

            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(post_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_post', post_id=post_id))

    else:
        return redirect(url_for('login'))


@app.route('/posts/<post_id>/likes', methods=['POST'])
def likeCounter(post_id):
    if session.get('user'):

        post = db.session.query(Post).filter_by(id=post_id).one()

        likes = post.likes

        likes = likes + 1

        post.likes = likes

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('get_post', post_id=post_id))

    else:
        return redirect(url_for('login'))


@app.route('/posts/<post_id>/dislikes', methods=['POST'])
def dislikeCounter(post_id):
    if session.get('user'):

        post = db.session.query(Post).filter_by(id=post_id).one()

        dislikes = post.dislikes

        dislikes = dislikes + 1

        post.dislikes = dislikes

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('get_post', post_id=post_id))

    else:
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
