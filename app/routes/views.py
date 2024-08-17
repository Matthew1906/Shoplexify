from flask import Blueprint, render_template, request
from sqlalchemy import select
from sqlalchemy.sql import func
from ..models import Category, Product, ProductCategory, ProductReview

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/<int:page>')
def home(page=1):
    rated_products = Product.query.join(Product.reviews).group_by(Product.id).order_by(func.avg(ProductReview.rating).desc())
    unrated_products = Product.query.filter(~Product.reviews.any())
    products = rated_products.union_all(unrated_products)
    return render_template('views.html', products = products.paginate(page, 9))

@views.route('/categories/<int:id>')
@views.route('/categories/<int:id>/pages/<int:page>')
def get_by_category(id, page=1):
    category = Category.query.filter_by(id=id).first()
    rated_products = Product.query.join(Product.reviews).join(ProductCategory).filter_by(category_id=id).group_by(Product.id).order_by(func.avg(ProductReview.rating).desc())
    unrated_products = Product.query.filter(~Product.reviews.any()).join(ProductCategory).filter_by(category_id=id)
    products = rated_products.union_all(unrated_products)
    return render_template('views.html', products= products.paginate(page, 9), category=id, category_name=category.name)

@views.route('/search')
@views.route('/<int:page>/search')
def search_product(page=1):
    query = request.args.get('search')
    rated_products = Product.query.filter(Product.name.ilike(f'%{query}%')).join(Product.reviews).group_by(Product.id).order_by(func.avg(ProductReview.rating).desc())
    unrated_products = Product.query.filter(~Product.reviews.any()).filter(Product.name.ilike(f'%{query}%'))
    products = rated_products.union_all(unrated_products)
    return render_template('views.html', products= products.paginate(page, 9))
    