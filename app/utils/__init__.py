from .decorators import admin_only, member_only
from .filters import utils
from .forms import CartForm, LoginForm, ProductForm, RegisterForm, ReviewForm, TransactionForm
from .notifications import get_notifications
from .payment_processing import get_payment_info

@utils.app_template_filter("all_notifications")
def all_notifications(user):
    return get_notifications(user)

@utils.app_template_filter("num_of_notifications")
def num_of_notifications(user):
    return len(get_notifications(user))
