from flask import Blueprint
from flask_login import current_user
from functools import wraps
from locale import currency

utils = Blueprint('utils', __name__)

# --------------------- Decorators ---------------------

def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.id == 1 :
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function

def member_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.id != 1 :
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function

# --------------------- Filters ---------------------

@utils.app_template_filter('format_currency')
def format_currency(price:int):
    '''Format currency'''
    return currency(float(price))

@utils.app_template_filter('format_date')
def format_date(date):
    '''Format Date'''
    return date.strftime('%d/%m/%Y')

@utils.app_template_filter('refactor_categories')
def refactor_categories(categories:list):
    '''Change the categories into a more readable string format'''
    if len(categories) == 0:
        return 'Miscellaneous'
    return ', '.join([pc.category.name.replace('And', ' & ') for pc in categories])

@utils.app_template_filter('get_stars')
def get_stars(rating:int):
    '''Convert Rating into stars'''
    return '★' * rating

@utils.app_template_filter('get_average_rating')
def get_average_rating(reviews):
    '''Get average rating and convert them into stars'''
    if len(reviews) == 0:
        return 'Not Rated'
    return '★' * (sum([review.rating for review in reviews]) // len(reviews))

@utils.app_template_filter('get_number_of_reviews')
def get_number_of_reviews(reviews):
    '''Convert Rating into stars'''
    return len(reviews)

@utils.app_template_filter('get_order_count')
def get_order_count(orders):
    '''Get number of products in total (from Order object)'''
    if type(orders) == list:
        return sum([order.get('quantity') for order in orders])
    else:
        return sum([order.quantity for order in orders])

@utils.app_template_filter('get_products_count')
def get_products_count(details):
    '''Get Number of products in total (from TransactionDetail object)'''
    return sum([detail.quantity for detail in details])

@utils.app_template_filter('get_current_sum')
def get_current_sum(orders):
    '''Get Temporary Total Cost in Cart (from Order object)'''
    if type(orders) == list:
        return currency(float(sum([order.get('product').price * order.get('quantity') for order in orders])))
    else:
        return currency(float(sum([order.product.price * order.quantity for order in orders])))

@utils.app_template_filter('get_price_sum')
def get_price_sum(transactions):
    '''Get Total Cost (from Transaction object)'''     
    return currency(float(sum([transaction.price * transaction.quantity for transaction in transactions])))

@utils.app_template_filter('get_total_payment')
def get_total_payment(info):
    '''Get Total Cost + Delivery Cost in currency format (from Transaction Object)'''
    return currency(float(info.delivery_cost+sum([transaction.price * transaction.quantity for transaction in info.details])))

@utils.app_template_filter('get_length')
def get_length(orders):
    '''Get length of orders'''
    if type(orders)==list:
        return len(orders)
    else:
        return orders.count()