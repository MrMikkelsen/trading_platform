from typing import List
from DB.models.orders import Order, OrderSchema
from DB.models.securities import Security
from DB.models.team import Team
from DB.models.completed_orders import CompletedOrder
from DB.session import get_session
from utils.time_simulator import time_con
from sqlalchemy import and_, func, desc, distinct, case, extract, or_
from sqlalchemy import func, select
import datetime
import sys


def get_all_pending_orders(team_id: int) -> list:
    """Get the open orders of a team"""
    with get_session() as session:

        # get all open orders where team_id == team_id
        open_orders = session.query(Order, Security.symbol).join(Security, Security.id == Order.security_id).filter(Order.team_id == team_id).filter(
            Order.order_status == 'pending').all()
        orders = []
        for order in open_orders:
            order_dict = OrderSchema().dump(order[0])
            order_dict.update({"symbol": order[1]})
            orders.append(order_dict)
        return orders


def get_all_completed_orders(team_id: int) -> list:
    """Get the completed orders of a team"""
    with get_session() as session:

        completed_orders = session.query(CompletedOrder, Security.symbol).join(
            Security, Security.id == CompletedOrder.security_id).filter(CompletedOrder.team_id == team_id).all()
        orders = []

        for order in completed_orders:
            order_dict = OrderSchema().dump(order[0])
            order_dict.update({"symbol": order[1]})
            orders.append(order_dict)
        return orders


def get_all_stoploss_orders(team_id: int) -> list:
    """Get stop loss orders of a team"""
    with get_session() as session:

        stoploss_orders = session.query(Order, Security.symbol).join(Security, Security.id == Order.security_id).filter(
            Order.team_id == team_id).filter(Order.order_type == "stoploss").filter(Order.order_status == "pending")

        orders = []

        for order in stoploss_orders:
            order_dict = OrderSchema().dump(order[0])
            order_dict.update({"symbol": order[1]})
            orders.append(order_dict)
        return orders


def get_average_traded_price(team_id: int, offset=0) -> dict:
    """Get average traded price of trades done on all Securities for a team"""
    with get_session() as session:
        # get all securities traded by a team
        securities = session.query(CompletedOrder.security_id, func.avg(CompletedOrder.price)).filter(
            CompletedOrder.team_id == team_id).group_by(CompletedOrder.security_id).all()

        result = {}
        try:
            for security_id, amount in securities:
                # get the symbol of the security
                symbol = session.query(Security.symbol).filter(
                    Security.id == str(security_id)).scalar()

                result[str(symbol)] = amount

        except Exception as e:
            print(e, file=sys.stderr)
        return result


def get_volume_completed_orders_history(team_id: int, offset: int) -> dict:
    """Get amount of stocks traded and how many trades have been done"""
    with get_session() as session:
        orders = session.query(CompletedOrder).filter(
            CompletedOrder.team_id == team_id)
        # apply offset to orders if necessary
        if offset > 0:
            current_time = time_con.get_current_time()
            date_now = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0)
            date_offset = date_now - datetime.timedelta(days=offset)
            orders = orders.filter(
                CompletedOrder.ended_at >= date_offset, CompletedOrder.ended_at <= date_now)
        # get amount of stocks traded and how many trades have been done
        return {
            'numberOfStocks': sum(order.amount for order in orders),
            'numberOfTrades': orders.count()
        }


def get_trade_history_unique_trades_offset(team_id, offset):
    """Get trading unique amount of trades in an offset of either daily, weekly or monthly data
    return:
        unique_trades: int
    """

    with get_session() as session:
        current_time = time_con.get_current_time()
        if offset == 0:
            unique_trades = session.query(func.count(distinct(CompletedOrder.security_id))).filter(
                CompletedOrder.ended_at <= current_time).filter(CompletedOrder.team_id == team_id).scalar()
        else:
            date_now = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0)
            date_offset = date_now - datetime.timedelta(days=offset)

            unique_trades = session.query(func.count(distinct(CompletedOrder.security_id))).filter(
                CompletedOrder.ended_at >= date_offset).filter(CompletedOrder.ended_at <= date_now)\
                .filter(CompletedOrder.team_id == team_id).scalar()

        return unique_trades


def get_avg_length_of_trade(team_id, offset):
    """
    Get average trading length of trades in an offset of either daily, weekly or monthly data
    Excludes weekdays
    return:
        average_trading_length : int
    """
    with get_session() as session:
        current_time = time_con.get_current_time()
        date_now = current_time.replace(
            hour=0, minute=0, second=0, microsecond=0)
        date_offset = date_now - datetime.timedelta(days=offset)

        if offset == 0:
            average_trading_length = (session.query(func.avg(
                func.date_part('day', CompletedOrder.ended_at -
                               CompletedOrder.created_at)
            ))
                .filter(CompletedOrder.ended_at <= current_time)
                .filter(CompletedOrder.team_id == team_id)
                .scalar())
        else:
            average_trading_length = (session.query(func.avg(
                func.date_part(
                    'day', CompletedOrder.ended_at - CompletedOrder.created_at)
            ))
                .filter(CompletedOrder.ended_at <= current_time)
                .filter(CompletedOrder.ended_at >= date_offset)
                .filter(CompletedOrder.ended_at <= date_now)
                .filter(CompletedOrder.team_id == team_id)
                .scalar())

        if average_trading_length is None:
            return 0
        else:
            return average_trading_length
# already exist version of this but hey...


def get_orders_pending(ticker: str = None) -> List[Order]:
    """Get all pending orders"""
    with get_session() as session:
        if ticker is None:
            orders = session.query(Order).filter(
                Order.order_status == 'pending').all()
        else:
            security = session.query(Security).filter(
                Security.symbol == ticker).first()
            orders = session.query(Order).filter(
                Order.order_status == 'pending').filter(Order.security_id == security.id).all()
        return orders
