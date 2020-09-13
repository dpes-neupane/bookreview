from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from create_books import *

db = SQLAlchemy()


user_reviews = db.Table('reviews',
     db.Column('reviewer', db.Integer, db.ForeignKey('Users.id')),
     db.Column( 'reviewed_book',db.Integer, db.ForeignKey('books.id')),
     db.Column('review_id', db.Integer, primary_key=True),
     db.Column( 'review',db.Text, nullable=False)
    )
     

class Users(db.Model):
    __tablename__= "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable= False)
    
    books_reviewed = db.relationship('books', secondary = user_reviews, backref=db.backref('reviewer', lazy=True), lazy='subquery')



class books(db.Model):
    __tablename__="books"
    id=db.Column(db.Integer,primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    name = db.Column(db.String,nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String,nullable=False)


    