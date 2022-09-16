from flask import Blueprint

utils = Blueprint('utils', __name__)

def currency(price:int):
    price_str = str(price)
    prefix_index = len(price_str)%3 if len(price_str)%3!=0 else 3
    prefix = price_str[:prefix_index]
    suffix = price_str[prefix_index:]
    return 'Rp' + prefix +''.join(["." + suffix[i*3:3*i+3] for i in range(len(price_str)//3) if suffix[i*3:i*3+3]!='']) + ',00'

@utils.app_template_filter('format_currency')
def format_currency(price:int):
    '''Format currency'''
    return currency(price)

@utils.app_template_filter('format_date')
def format_date(date):
    '''Format Date'''
    return date.strftime('%d/%m/%Y')

@utils.app_template_filter('format_category')
def format_category(category):
    '''Format Date'''
    return category.replace("And", " & ")

@utils.app_template_filter("format_notification")
def format_notification(notification):
    return f"<span class='fw-bold {notification.get('color')}'>{'Completed' if notification.get('status') else 'Unpaid'}</span> transaction on {notification.get('date').strftime('%d/%m/%Y')}"

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
    return sum([order.quantity for order in orders])

@utils.app_template_filter('get_products_count')
def get_products_count(details):
    '''Get Number of products in total (from TransactionDetail object)'''
    return sum([detail.quantity for detail in details])

@utils.app_template_filter('get_current_sum')
def get_current_sum(orders):
    '''Get Temporary Total Cost in Cart (from Order object)'''
    return currency(sum([order.product.price * order.quantity for order in orders]))

@utils.app_template_filter('get_price_sum')
def get_price_sum(transactions):
    '''Get Total Cost (from Transaction object)'''     
    return currency(sum([transaction.price * transaction.quantity for transaction in transactions]))

@utils.app_template_filter('get_total_payment')
def get_total_payment(info):
    '''Get Total Cost + Delivery Cost in currency format (from Transaction Object)'''
    return currency(info.delivery_cost+sum([transaction.price * transaction.quantity for transaction in info.details]))
    