from flask import Blueprint, render_template, request
from ..models import Product, ProductCategory

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/<int:page>')
def home(page=1):
    products = Product.query.paginate(page,9)
    return render_template('index.html', products = products)

@views.route('/category/<int:id>')
@views.route('/category/<int:id>/<int:page>')
def get_by_category(id:int, page=1):
    products = Product.query.join(ProductCategory).filter_by(category_id=id).paginate(page,9)
    return render_template('index.html', products= products)

@views.route('/search')
@views.route('/search/<int:page>')
def search_product(page=1):
    query = request.args.get('search')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).paginate(page,9)
    return render_template('index.html', products= products)