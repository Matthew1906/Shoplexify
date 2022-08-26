from flask import Blueprint, render_template, request
from ..models import Category, Product, ProductCategory

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/<int:page>')
def home(page=1):
    products = Product.query.paginate(page,9)
    return render_template('views.html', products = products)

@views.route('/categories/<id>')
@views.route('/categories/<id>/pages/<int:page>')
def get_by_category(id, page=1):
    category = Category.query.filter_by(id=id).first()
    products = Product.query.join(ProductCategory).filter_by(category_id=id).paginate(page,9)
    return render_template('views.html', products= products, category=id, category_name=category.name)

@views.route('/search')
@views.route('/<int:page>/search')
def search_product(page=1):
    query = request.args.get('search')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).paginate(page,9)
    return render_template('views.html', products= products)
    