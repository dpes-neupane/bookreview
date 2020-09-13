from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import csv
from create_books import *



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://wbrsrzqbgxwxqx:4756fbfea10fcbbb006d3f18a8f02a4990278316305a3f0465870496c55b083f@ec2-174-129-254-238.compute-1.amazonaws.com:5432/d5dafq9punt1dn")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    count = 0
    for isbn, title, author, year in reader:
        title = title.lower()
        author = author.lower()
        db.execute("INSERT INTO Books (isbn, name, author, year) VALUES (:isbn, :name, :author, :year)",
                    {"isbn": isbn, "name": title, "author": author, "year": year}) 
        count += 1
        print(f" {count} Added  to isbn: {isbn} title: {title} author: {author} Year: {year}.")
        db.commit()


if __name__ == "__main__":
    main()
        