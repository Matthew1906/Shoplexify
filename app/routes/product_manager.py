from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from .. import db
from ..models import Category, Order, Product, ProductCategory, ProductReview, Transaction, TransactionDetail
from ..utils import admin_only, CartForm, ProductForm, ReviewForm

product_manager = Blueprint('product_manager', __name__)

@product_manager.route('/products/add', methods=['GET','POST'])
@admin_only
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        find_product = Product.query.filter_by(name=request.form.get('name')).first()
        if find_product is None:
            new_product = Product(
                name = request.form.get('name'),
                description = request.form.get('description'),
                image_url = request.form.get('image_url'),
                price = request.form.get('price'),
                stock = request.form.get('stock'),
            )
            db.session.add(new_product)
            db.session.commit()
            for category in form.categories.data:
                new_product_category = ProductCategory(
                    product = new_product,
                    category = Category.query.filter_by(name=category).first()
                )
            db.session.add(new_product_category)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template('product_manager.html', purpose = 'add', form = form)

@product_manager.route('/products/<int:id>/update', methods=['GET', 'POST'])
@admin_only
def update_product(id):
    product = Product.query.filter_by(id=id).first()
    form = ProductForm(
        name = product.name,
        description=product.description,
        image_url=product.image_url,
        price = product.price,
        stock = product.stock,
        categories = [category for category in product.categories]
    )
    if form.validate_on_submit():
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.image_url = request.form.get('image_url')
        product.price = request.form.get('price')
        product.stock = request.form.get('stock')
        categories = ProductCategory.query.filter_by(product_id=id)
        for category in categories:
            db.session.delete(category)
            db.session.commit()
        for category in form.categories.data:
            new_product_category = ProductCategory(
                product = product,
                category = Category.query.filter_by(name=category).first()
            )
            db.session.add(new_product_category)
            db.session.commit()
        return redirect(url_for('product_manager.get_product', id=id))
    return render_template('product_manager.html', product=product, purpose = 'update', form = form)

@product_manager.route('/products/<int:id>', methods=['GET', 'POST'])
def get_product(id):
    # Get product object
    product = Product.query.filter_by(id=id).first()
    # Get product recommendations
    recommendations = Product.query.filter(Product.id!=id)\
        .join(Product.reviews, isouter=True).join(Product.categories, isouter=True)\
            .order_by(ProductReview.rating.desc())
    if product.categories!=[]:
        product_categories = set([cat.category for cat in product.categories])
        filter_categories = lambda x:list(set([cat.category for cat in x.categories]).intersection(product_categories))!=[]
        similar_products = list(filter(filter_categories, recommendations))[:9]
        similar_products+=list(set(recommendations)-set(similar_products))[:9-len(similar_products)]
    else:
        similar_products = recommendations[:9]
    similar_products.sort(key=lambda x:(sum([review.rating for review in x.reviews]) // len(x.reviews)) if len(x.reviews)!=0 else 0, reverse=True)
    # Get cart status (if the user is logged in, it will check his/her orders)
    count_order = Order.query.filter_by(user_id = current_user.id, product_id=id).first() if current_user.is_authenticated else None
    cart_form = CartForm(
        count= count_order.quantity if current_user.is_authenticated and count_order!=None else 1, 
        limit=product.stock
    )
    # Check if the user is allowed to give reviews
    product_transactions = db.session.execute(
        select(Transaction.user_id).join(Transaction.details).where(TransactionDetail.product_id==id)
    ).scalars().all()
    review_form = ReviewForm()
    if current_user.is_authenticated and review_form.validate_on_submit():
        find_product_review = ProductReview.query.filter_by(product=product, user=current_user).first()
        if find_product_review:
            db.session.delete(find_product_review)
            db.session.commit()
        new_product_review = ProductReview(
            user = current_user,
            product = product,
            rating = int(request.form.get('rating')),
            review = request.form.get('body')
        )
        db.session.add(new_product_review)
        db.session.commit()
        return redirect(url_for('product_manager.get_product', id=id))
    return render_template(
        'product_manager.html',
        cart_form=cart_form, 
        review_form=review_form, 
        product=product, 
        purpose = 'get',
        valid_review=current_user.id in product_transactions if current_user.is_authenticated else False,
        recommendations=similar_products
    )
