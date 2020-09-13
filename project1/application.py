import os
from models import *
from create_books import *
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select 
import requests



app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://wbrsrzqbgxwxqx:4756fbfea10fcbbb006d3f18a8f02a4990278316305a3f0465870496c55b083f@ec2-174-129-254-238.compute-1.amazonaws.com:5432/d5dafq9punt1dn")
db = scoped_session(sessionmaker(bind=engine))





#set up the index page:
@app.route('/')
def index():
    
    return render_template('index.html')


#setting up a registration page:
@app.route('/signup', methods = ("GET","POST"))
def signup():
    if request.method == "POST":  
        username = request.form["name"]
        password = request.form["password"]
        error = None
        select = Users.query.filter_by(name=username).first()
        if not username:
            error = "Name is Required!"
        elif not password:
            error = "Password is Required!"
        elif select is not None:
            error = f'{username} already exists'
        if error is None:
            user = Users(name=username,password=password)
            db.add(user)
            db.commit()
            return redirect(url_for('index'))
        flash(error)
        
    return render_template('signup.html')
        

@app.route('/login', methods=("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        error = None
        user = Users.query.filter_by(name=username).first()
        if user is None:
            error = "Please enter a valid Name"
        if user is not None:
            word = user.password
            if word != password:
                error = "Please enter the correct password!"
        if error is None:
            session.clear()
            session['user_id'] = user.id
            
            return redirect(url_for('index'))
        flash(error)
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=("GET","POST"))
def search():
    if request.method == "POST":
        error = None
        name = request.form["name"].lower()
        
        temp = books.query.filter(or_( or_(books.name.like(name + '%'), books.author.like(name + '%')) , books.isbn.like(name + '%'))).all()
        
        if not temp:
            error = "no BOOK!"
        if error is None:
            return render_template("search.html", book=temp)
        flash(error)
    return render_template("search.html")

@app.route('/search/<string:name>', methods=("GET","POST"))
def book(name):
    rviews = None
    flag = None
    sec = None
    per = None
    user_r = None
    book = books.query.filter(or_( or_(books.name.like(name + '%'), books.author.like(name + '%')) , books.isbn.like(name + '%'))).first()
    data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "3ndnyVAOXIXLTE6CSpBpkA", "isbns": book.isbn})
    res = data.json()
    
    user_name = Users.query.filter_by(id=session['user_id']).first()
    
    sec = select([user_reviews]).where(user_reviews.c.reviewed_book == book.id )
    second = db.execute(sec)
    rep = second.fetchall()
    if rep == []:
        flag = 'There are no reviews!'
    
    
    if request.method == "POST": 
        user_r = request.form["review"]
        user = session['user_id']
        r = db.execute(select([user_reviews]).where(and_(user_reviews.c.reviewed_book == book.id, user_reviews.c.reviewer == session['user_id']) ))
        per = r.fetchall()
        if user_r is not None: 
            if per == [] :
                ins = user_reviews.insert().values(review=user_r, reviewer=user, reviewed_book=book.id) 
                engine.connect().execute(ins)
                return redirect(url_for('book'))  
                
    return render_template("book.html", book=book, data=res, reviews=rviews, user_name=user_name, flag=flag, rep=rep, per=per, user_r=user_r, Users=Users)


