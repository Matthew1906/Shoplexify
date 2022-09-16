from datetime import date
from sqlalchemy import and_, or_
from ..models import Transaction

def get_notifications(user):
    transactions = Transaction.query.filter(and_(Transaction.user_id==user.id,
        or_(Transaction.date == date.today(), Transaction.payment_status=='Unpaid')))\
                .order_by(Transaction.date.desc())
    return [{"id":tr.id, "date":tr.date, "status": tr.payment_status=='Paid', "color":"text-success" if tr.payment_status=='Paid' else "text-danger"} for tr in transactions]