from datetime import datetime
from os import getenv
import midtransclient

def get_payment_info(current_user, transaction):
    server_key = getenv('SERVER_KEY')
    client_key = getenv("CLIENT_KEY")
    # Initialize Snap
    snap = midtransclient.Snap(
        is_production=False,
        server_key=server_key,
        client_key=client_key
    )
    params = {
        'transaction_details':{
            'order_id': f'ORDER_{transaction.id}_' + datetime.now().strftime('%Y-%m-%d-%H.%M.%S'),
            'gross_amount':sum([detail.quantity*detail.price for detail in transaction.details]) + transaction.delivery_cost
        },
        'item_details':[{
            'name':detail.product.name,
            'categories':[category.category.name for category in detail.product.categories],
            'price':detail.price,
            'quantity':detail.quantity
        } for detail in transaction.details]\
            .append({
                'name':'Delivery Cost',
                'price': transaction.delivery_cost,
                'quantity':1
            }),
        'customer_details':{ 
            'email':current_user.email
        },
        'enabled_payments':["credit_card",
            "bca_klikbca", "bri_epay", "echannel", "permata_va",
            "bca_va", "bni_va", "bri_va", "other_va", "gopay","shopeepay"
        ],
    }
    transaction_token = snap.create_transaction_token(params)
    return transaction_token, client_key