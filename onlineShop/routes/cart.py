from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from .. import db
from ..models import Order, Product
from ..utils import member_only

cart = Blueprint('cart', __name__)

@cart.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if int(request.form.get('count')) > product.stock:
        return redirect(url_for('views.home'))
    if current_user.is_authenticated and current_user.id !=1:
        new_order = Order(
            user= current_user,
            product = product,
            quantity = int(request.form.get('count'))
        )
        product.stock-=new_order.quantity
        db.session.add(new_order)
        db.session.commit()
    else:
        if 'orders' in session:
            orders = session['orders']
        else:
            orders = []
        orders.append({'product':product.id, 'quantity':int(request.form.get('count'))})
        session['orders'] = orders
    return redirect(url_for('views.home'))

@cart.route('/cart')
def get_cart():
    if current_user.is_authenticated and current_user.id!=1:
        orders = Order.query.filter_by(user=current_user)
    else:
        orders = [] 
        if 'orders' in session:
            for order in session['orders']:
                product = Product.query.filter_by(id = order['product']).first()
                orders.append({'product':product, 'quantity':order['quantity']})
    return render_template('cart.html', orders = orders)

@cart.route('/cart/increment_quantity/<int:product_id>')
def increment_product_quantity(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if current_user.is_authenticated and current_user.id!=1:
        order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
        order.quantity+=1
        product.stock-=1
        db.session.commit()
    else:
        order = session['orders'][[idx for idx, vals in enumerate(session['orders'])  if vals['product'].id == product_id][0]]
        order['quantity'] += 1
        product.stock-=1
    return redirect(url_for('cart.get_cart'))

@cart.route('/cart/decrement_quantity/<int:product_id>')
def decrement_product_quantity(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if current_user.is_authenticated and current_user.id!=1:
        order = Order.query.filter_by(user_id=user_id, product_id=product_id).first()
        order.quantity-=1
        product.stock+=1
        db.session.commit()
    else:
        order = session['orders'][[idx for idx, vals in enumerate(session['orders'])  if vals['product'].id == product_id][0]]
        order['quantity'] -= 1
        product.stock+=1
    return redirect(url_for('cart.get_cart'))