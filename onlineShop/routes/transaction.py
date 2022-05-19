from datetime import datetime
from flask import abort, Blueprint, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required
from json import loads
from .. import db
from ..forms import TransactionForm
from ..models import Order, Transaction, TransactionDetail
from ..payment_processing import get_payment_info
from ..utils import member_only


transaction = Blueprint('transaction', __name__)

@transaction.route('/cart/<int:user_id>/checkout', methods=['GET', 'POST'])
@login_required
@member_only
def checkout(user_id):
    if user_id != current_user.id:
        return abort(403)
    details = Order.query.filter_by(user=current_user)
    transaction_id = 0
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            user = current_user,
            date = datetime.now().date(),
            payment_method = 'Untold',
            payment_status = 'Unpaid',
            address = request.form.get('address'),
            delivery_cost = len(request.form.get('address'))*100,
            delivery_status = 'Unsent',
        )
        db.session.add(new_transaction)
        db.session.commit()
        for detail in details:
            new_transaction_detail = TransactionDetail(
                transaction = new_transaction,
                product = detail.product,
                quantity = detail.quantity,
                price = detail.product.price
            )
            db.session.add(new_transaction_detail)
            db.session.commit()
        transaction_id = new_transaction.id 
        for detail in details:
            db.session.delete(detail)
            db.session.commit() 
        return redirect(url_for(
            endpoint='transaction.get_transaction_history', 
            user_id = user_id, 
            transaction_id = transaction_id
        ))    
    return render_template('checkout.html', form=form, details=details, purpose = 'checkout-info')

@transaction.route('/history/<int:user_id>')
@login_required
@member_only
def get_all_transactions(user_id):
    if user_id != current_user.id:
        return abort(403)
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc())
    return render_template('transaction.html', transactions = transactions, purpose='show_all')

@transaction.route('/history/<int:user_id>/transactions/<int:transaction_id>', methods=['GET'])
@login_required
@member_only
def get_transaction_history(user_id, transaction_id):
    if user_id != current_user.id:
        return abort(403)
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    token, client_key = get_payment_info(current_user, transaction)
    return render_template('transaction.html', transaction = transaction, purpose='single', token=token, client_key=client_key)

def get_transaction_id(id_str:str):
    return int(id_str.split("_")[1])

@transaction.route("/payment/notifications", methods=['POST'])
@login_required
@member_only
def get_payment_notifications():
    transaction_id = get_transaction_id(request.form.get('order_id'))
    payment_method = request.form.get('payment_type')
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    transaction.delivery_status = 'Delivered'
    transaction.payment_status = 'Paid'
    transaction.payment_method = payment_method
    db.session.commit()  
    return redirect(url_for('transaction.get_transaction_history', user_id=current_user.id, transaction_id=transaction_id))