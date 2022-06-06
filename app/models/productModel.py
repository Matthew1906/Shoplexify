# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config table
class Product(db.Model):
    '''Product Table'''
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    image_url = db.Column(db.String(5000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    orders = relationship('Order', back_populates='product')
    reviews = relationship('ProductReview', back_populates='product')   
    transaction_details = relationship('TransactionDetail', back_populates='product')
    categories = relationship('ProductCategory', back_populates='product')
