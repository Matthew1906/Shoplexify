from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import current_user
from .. import db
from ..models import Order, Product

cart = Blueprint('cart', __name__)

@cart.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if int(request.form.get('count')) > product.stock:
        return redirect(url_for('views.home'))
    if current_user.is_authenticated and current_user.id !=1:
        order = Order.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if order != None:
            order.quantity+=int(request.form.get('count'))
        else:
            new_order = Order(
                user= current_user,
                product = product,
                quantity = int(request.form.get('count'))
            )
            db.session.add(new_order)
    else:
        if 'orders' in session:
            orders = session['orders']
        else:
            orders = []
        orders.append({'product':product.id, 'quantity':int(request.form.get('count'))})
        session['orders'] = orders
    product.stock-=int(request.form.get('count'))
    db.session.commit()
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
        order = Order.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        order.quantity+=1
    else:
        orders = session['orders']
        for order in orders:
            if order['product']==product_id:
                res_order = order
                break
        res_order['quantity'] += 1
        session['orders'] = orders
    product.stock-=1
    db.session.commit()
    return redirect(url_for('cart.get_cart'))

@cart.route('/cart/decrement_quantity/<int:product_id>')
def decrement_product_quantity(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if current_user.is_authenticated and current_user.id!=1:
        order = Order.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        order.quantity-=1
        if order.quantity<=0:
            db.session.delete(order)
    else:
        orders = session['orders']
        for order in orders:
            if order['product']==product_id:
                res_order = order
                break
        res_order['quantity'] -= 1
        if res_order['quantity']<=0:
            orders.remove(res_order)
        session['orders'] = orders
    product.stock+=1
    db.session.commit()
    return redirect(url_for('cart.get_cart'))
