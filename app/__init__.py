from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from locale import setlocale, LC_ALL
from os import getenv, path
from pandas import read_csv
from slugify import slugify
from werkzeug.security import generate_password_hash

# Create Database
db = SQLAlchemy()

# Load Environment Variables
load_dotenv()

# Configure Locale
# setlocale(LC_ALL, 'id_ID.utf8')

def create_app():
    # Create App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    # Config Database URL
    if getenv('DATABASE_URL') == None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///online-shop.db'
    else: 
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Database
    db.init_app(app)
    
    from .utils import utils
    app.register_blueprint(utils)

    from .routes.auth import auth
    app.register_blueprint(auth)

    from .routes.cart import cart
    app.register_blueprint(cart)

    from .routes.product_manager import product_manager
    app.register_blueprint(product_manager)
    
    from .routes.transaction import transaction
    app.register_blueprint(transaction)

    from .routes.views import views
    app.register_blueprint(views)

    # Uncomment for initial data
    # create_database(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Import User Model
    from .models import User

    # Default loading user function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

def create_database(app):
    # create database
    db.create_all(app=app)    
    # insert initial values 
    from .models import Category, User
    with app.app_context():
        categories = read_csv('./resources/categories.csv', delimiter=";")
        products = read_csv('./resources/products.csv', delimiter=';')
        product_categories = read_csv("./resources/product_categories.csv", delimiter=";")
        reviews = read_csv('./resources/reviews.csv', delimiter=";")
        transactions = read_csv("./resources/transactions.csv", delimiter=";")
        transaction_details = read_csv('./resources/transaction_details.csv', delimiter=";")
        users = read_csv("./resources/users.csv", delimiter=";")
        categories.to_sql(name='categories', con=db.engine, if_exists='append', index=False)
        products.to_sql(name='products', con=db.engine, if_exists='append', index=False)
        product_categories.to_sql(name='product_categories', con=db.engine, if_exists='append', index=False)
        users.to_sql(name='users', con=db.engine, if_exists='append', index=False)
        reviews.to_sql(name='reviews', con=db.engine, if_exists='append', index=False)
        transactions.to_sql(name='transactions', con=db.engine, if_exists='append', index=False)
        transaction_details.to_sql(name='transaction_details', con=db.engine, if_exists='append', index=False)
