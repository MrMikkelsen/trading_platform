from DB.models.securities import Security
from DB.models.orders import Order, OrderSchema
from DB.models.completed_orders import CompletedOrder
from DB.models.team import Team
from DB.models.holdings import Holding
from DB.session import get_session
from utils.time_simulator import time_con
from utils.exchange import prices_con
from utils.time_simulator import time_con
import datetime as dt

ARBITRARY_HIGH_AMOUNT = 1337*1000


def _place_order(symbol, amount, price_input, order_type, days_till_cancel, api_key):
    """ Place an order on given ticker and amount """
    try:
        symbol = symbol.upper()
        amount = int(amount)
        if amount < 0:
            raise Exception("Amount cannot be negative")

        order_type = order_type.lower()
        price = None
        if price_input is None:
            if order_type == "stoploss":
                raise Exception("Stoploss order must have a price")
            price = prices_con.get_current_price_for_ticker(symbol)
        else:
            price = float(price_input)
            if price < 0:
                raise Exception("Price cannot be negative")

        days_till_cancel = int(
            days_till_cancel) if days_till_cancel is not None else 30  # default 30 days
        if days_till_cancel < 0:
            raise Exception("Days till cancel cannot be negative")

    except ValueError:
        raise Exception("Invalid input: Non-integer value provided")
    except:
        raise Exception("Invalid input")

    try:
        with get_session() as session:
            team = session.query(Team).filter(
                Team.api_key == api_key).first()
            security = session.query(Security).filter(
                Security.symbol == symbol).first()

            if (price_input is None and price is not None):  # COMPLETED ORDER
                order = CompletedOrder(team_id=team.id, security_id=security.id,
                                       amount=amount, price=price,
                                       order_type=order_type, created_at=time_con.get_current_time())
                order.order_status = "completed"
                order.ended_at = time_con.get_current_time()
            else:  # PENDING ORDER
                order = Order(team_id=team.id, security_id=security.id,
                              amount=amount, price=price,
                              order_type=order_type, created_at=time_con.get_current_time(),
                              days_till_cancel=days_till_cancel)
                date, price = prices_con.datetime_for_price(session, order)

                if date is not None:
                    date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

                    # If the order will be possible in future, send it to the process worker
                    # Pending
                    order.future_striking_date = date
                    order.future_striking_price = price

            session.add(order)
            session.commit()
            return OrderSchema().dump(order)
    except Exception as e:
        raise Exception(e)


def _cancel_order(order_id, api_key):
    """ Cancel an order on order_id """
    try:
        with get_session() as session:
            team = session.query(Team).filter(
                Team.api_key == api_key).first()
            order = session.query(Order).filter(
                Order.id == order_id).first()
            if order.team_id == team.id:
                # update order
                order.order_status = "cancelled"
                order.ended_at = time_con.get_current_time()
                order_return = {
                    "message": "Order cancelled",
                    "order": OrderSchema().dump(order)

                }
                session.commit()
                return order_return
            else:
                raise Exception("order does not belong to team")
    except Exception as e:
        raise Exception(e)
