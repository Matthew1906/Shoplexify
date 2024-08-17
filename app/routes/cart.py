from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .. import db
from ..models import Order, Product, ProductReview
from ..utils import member_only

cart = Blueprint('cart', __name__)

@cart.route('/cart/<int:user_id>/products/<int:product_id>', methods=['POST'])
@login_required
@member_only
def add_to_cart(user_id, product_id):
    '''Add product to the cart'''
    product = Product.query.filter_by(id=product_id).first()
    if int(request.form.get('count')) > product.stock:
        return redirect(url_for('views.home'))
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    prev_quantity = 0
    if order != None:
        prev_quantity=order.quantity
        order.quantity = int(request.form.get('count'))
    else:
        order = Order(
            user= current_user,
            product = product,
            quantity = int(request.form.get('count'))
        )
        db.session.add(order)
    product.stock-=int(request.form.get('count'))-prev_quantity
    if order.quantity == 0:
        db.session.delete(order)
    db.session.commit()
    return redirect(url_for('product_manager.get_product', id=product_id))

@cart.route('/cart/<int:user_id>/products/<int:product_id>/delete')
@login_required
@member_only
def delete_from_cart(user_id, product_id):
    '''Delete product from cart'''
    product = Product.query.filter_by(id=product_id).first()
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    if order != None:
        product.stock += order.quantity
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('cart.get_cart', user_id=user_id))

@cart.route('/cart/<int:user_id>')
@login_required
@member_only
def get_cart(user_id):
    '''Get user's cart'''
    orders = Order.query.filter_by(user_id=user_id)
    recommendations = list(filter(lambda x:x.id not in [order.product.id for order in orders], Product.query.all()))
    recommendations.sort(key=lambda x:(sum([review.rating for review in x.reviews]) // len(x.reviews)) if len(x.reviews)!=0 else 0, reverse=True)
    return render_template('cart.html', orders = orders, recommendations=recommendations[:9])

@cart.route('/cart/<int:user_id>/clear')
@login_required
@member_only
def clear_cart(user_id):
    '''Clear user's cart'''
    orders = Order.query.filter_by(user_id=user_id)
    for order in orders:
        db.session.delete(order)
    db.session.commit()
    return redirect(url_for('views.home'))

@cart.route('/cart/<int:user_id>/products/<int:product_id>/increment')
def increment_product_quantity(user_id, product_id):
    '''Increase product quantity in user's order'''
    product = Product.query.filter_by(id=product_id).first()
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    order.quantity+=1
    product.stock-=1
    db.session.commit()
    return redirect(url_for('cart.get_cart', user_id=user_id))

@cart.route('/cart/<int:user_id>/products/<int:product_id>/decrement')
def decrement_product_quantity(user_id, product_id):
    '''Decrease product quantity in user's order'''
    product = Product.query.filter_by(id=product_id).first()
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    order.quantity-=1
    product.stock+=1
    db.session.commit()
    return redirect(url_for('cart.get_cart', user_id=user_id))
