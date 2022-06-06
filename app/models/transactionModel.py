# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config table
class Transaction(db.Model):
    '''Transaction table'''
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user = relationship('User', back_populates='transactions')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    details = relationship('TransactionDetail', back_populates='transaction')
    payment_method = db.Column(db.String(255), nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(5000), nullable=False)
    delivery_cost = db.Column(db.Integer, nullable=False)
    delivery_status = db.Column(db.String(255), nullable=False)
    
class TransactionDetail(db.Model):
    '''Details regarding transaction'''
    __tablename__ = 'transaction_details'
    transaction = relationship('Transaction', back_populates='details')
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    product = relationship('Product', back_populates='transaction_details')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    