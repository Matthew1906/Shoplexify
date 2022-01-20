from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .. import db
from ..models import Order, Product
from ..utils import member_only

cart = Blueprint('cart', __name__)

@cart.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id, user_id):
    product = Product.query.filter_by(id=product_id).first()
    if int(request.form.get('count')) > product.stock:
        return redirect(url_for('views.home'))
    new_order = Order(
        user= current_user,
        product = product,
        quantity = int(request.form.get('count'))
    )
    product.stock-=new_order.quantity
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('views.home'))

@cart.route('/cart/<int:user_id>')
@login_required
@member_only
def get_cart(user_id):
    orders = Order.query.filter_by(user=current_user)
    if user_id != current_user.id:
        return abort(403)
    return render_template('cart.html', orders = orders)

@cart.route('/cart/<int:user_id>/increment_quantity/<int:product_id>')
@login_required
@member_only
def increment_product_quantity(user_id, product_id):
    if user_id != current_user.id:
        return abort(403)
    product = Product.query.filter_by(id=product_id).first()
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    order.quantity+=1
    product.stock-=1
    db.session.commit()
    return redirect(url_for('cart.get_cart', user_id=user_id))

@cart.route('/cart/<int:user_id>/decrement_quantity/<int:product_id>')
@login_required
@member_only
def decrement_product_quantity(user_id, product_id):
    if user_id != current_user.id:
        return abort(403)
    product = Product.query.filter_by(id=product_id).first()
    order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
    order.quantity-=1
    product.stock+=1
    if order.quantity == 0:
        db.session.delete(order)
    db.session.commit()
    return redirect(url_for('cart.get_cart', user_id=user_id))