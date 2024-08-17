# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config tables
class Category(db.Model):
    '''Category table'''
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    product_categories = relationship('ProductCategory', back_populates ='category')

class ProductCategory(db.Model):
    '''Product categories'''
    __tablename__ = 'product_categories'
    product = relationship('Product', back_populates='categories')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    category = relationship('Category', back_populates='product_categories')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    