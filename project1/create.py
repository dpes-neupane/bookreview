import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://wbrsrzqbgxwxqx:4756fbfea10fcbbb006d3f18a8f02a4990278316305a3f0465870496c55b083f@ec2-174-129-254-238.compute-1.amazonaws.com:5432/d5dafq9punt1dn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    
    db.create_all()

if __name__ == "__main__":
    
    with app.app_context():
        main()