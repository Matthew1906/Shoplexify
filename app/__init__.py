from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from locale import setlocale, LC_ALL
from os import getenv, path
from pandas import read_csv

# Create Database
db = SQLAlchemy()

# Load Environment Variables
load_dotenv()

# Configure Locale
setlocale(LC_ALL, 'id_ID.utf8')

def create_app():
    # Create App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

    # Config Database URL
    if getenv('DATABASE_URL') == None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///online-shop.db'
    else: 
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL').replace("postgres", "postgresql")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Database
    db.init_app(app)
    
    from .utils import utils
    app.register_blueprint(utils, url_prefix='/')

    from .routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .routes.cart import cart
    app.register_blueprint(cart, url_prefix='/')

    from .routes.product_manager import product_manager
    app.register_blueprint(product_manager, url_prefix='/')
    
    from .routes.transaction import transaction
    app.register_blueprint(transaction, url_prefix='/')

    from .routes.views import views
    app.register_blueprint(views, url_prefix='/')

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
    from .models import Category
    with app.app_context():
        categories=[
            'Automotive','ArtsAndCrafts', 'Books', 'Clothing', 'Electronics', 
            'Food', 'HealthAndBeauty', 'HomeAndGarden', 'Office', 'SportsAndOutdoor'
        ]
        for category in categories:
            new_category = Category(name=category)
            db.session.add(new_category)
        db.session.commit()
        df = read_csv('./resources/products.csv', delimiter=';')
        df.to_sql(name='products', con=db.engine, if_exists='append', index=False)
