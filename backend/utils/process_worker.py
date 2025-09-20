from celery import shared_task
from DB.functions.teams import all_group_update_profit_history
from DB.models.orders import Order
from DB.session import get_session
from utils.time_simulator import time_con

'''
These tasks are run by celery worker

'''


@shared_task
def process_order():
    current_time = time_con.get_current_time()
    with get_session() as session:
        orders = session.query(Order).filter(
            Order.order_status == 'pending').all()
        for order in orders:
            if order.future_striking_date is not None and \
                    order.future_striking_date <= current_time:
                order.order_status = 'completed'
                order.ended_at = current_time
                order.price = order.future_striking_price

            elif order.cancel_date is not None and \
                    order.cancel_date <= current_time:
                order.order_status = 'cancelled'
                order.ended_at = current_time

        session.commit()


@shared_task
def update_profit_history():
    current_time = time_con.get_current_time()
    all_group_update_profit_history(current_time)
