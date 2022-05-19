# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config table
class Order(db.Model):
    '''Cart containing Products'''
    __tablename__ = 'orders'
    user = relationship('User', back_populates='cart')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    product = relationship('Product', back_populates='orders')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    