from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from .. import db
from ..forms import CartForm, ProductForm, ReviewForm
from ..models import Category, Product, ProductCategory, ProductReview
from ..utils import admin_only

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

@product_manager.route('/products/update/<int:id>', methods=['GET', 'POST'])
@admin_only
def update_product(id:int):
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
def get_product(id:int):
    product = Product.query.filter_by(id=id).first()
    cart_form = CartForm(product.stock)
    review_form = ReviewForm()
    if current_user.is_authenticated and review_form.validate_on_submit():
        find_product_review = ProductReview.query.filter_by(product=product, user=current_user).first()
        if find_product_review:
            with app.app_context():
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
        purpose = 'get'
    )
