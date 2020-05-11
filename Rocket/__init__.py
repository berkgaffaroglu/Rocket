from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#Setting up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bLq6HxQQ0r9bFnqm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#Importing the routes
from Rocket import routes
