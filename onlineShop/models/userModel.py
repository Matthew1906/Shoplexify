# Database
from .. import db 
from sqlalchemy.orm import relationship 
from flask_login import UserMixin

# Config table
class User(db.Model, UserMixin):
    '''User Table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    cart = relationship('Order', back_populates='user')
    reviews = relationship('ProductReview', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
