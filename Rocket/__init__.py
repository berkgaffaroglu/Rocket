from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#Setting up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bLq6HxQQ0r9bFnqm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#Importing the routes
from Rocket import routes
