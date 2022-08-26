# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config table
class ProductReview(db.Model):
    '''Product Review Table'''
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship('User', back_populates='reviews')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = relationship('Product', back_populates='reviews')
    product_id = db.Column(db.String(255), db.ForeignKey('products.id'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(5000), nullable=False)
    