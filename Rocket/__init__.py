from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#Setting up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bLq6HxQQ0r9bFnqm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#change that
app.config['MAIL_USERNAME'] = 'emailbot321@gmail.com'
app.config['MAIL_PASSWORD'] = '1250501974'
mail = Mail(app)



#Importing the routes
from Rocket import routes
