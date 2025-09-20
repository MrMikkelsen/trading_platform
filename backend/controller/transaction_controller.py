from flask import jsonify, request, Blueprint
from DB.models.orders import OrderSchema
from DB.functions.orders import get_orders_pending
from utils.security import api_required
from utils.brooker import _place_order, _cancel_order
import psycopg2.errors

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/', methods=['POST'])
@api_required
def order():
    """
    :param type: type of the order
    :param symbol: symbol of the stock
    :param amount: amount of the stock
    :param price: price of the stock
    :return: json with the order
    """
    # get api_key from request
    api_key = request.json.get("api_key")
    # get parameters from query string
    ticker = request.args.get('ticker')
    amount = request.args.get('amount')
    price = request.args.get('price')
    type = request.args.get('type')
    days_to_cancel = request.args.get('days_to_cancel')
    # try call place_order, if error return error as json
    try:
        order = _place_order(ticker, amount, price, type,
                             days_to_cancel, api_key)
        return jsonify(order), 200
    except psycopg2.errors.RaiseException as e:
        return {"message": str(e)}, 400
    except Exception as error:
        str_error = str(error)
        # TODO: Better error handling
        # i fixed with even more if statements :)
        if "set stoploss" in str_error:
            return {"message": "Not enough stock to set stoploss"}, 400
        elif "stock to sell" in str_error:
            return {"message": "Not enough stock to sell"}, 400
        elif "saldo to buy" in str_error:
            return {"message": "Not enough saldo to buy"}, 400
        elif "Stoploss order must have a price" in str_error:
            return {"message": "Stoploss order must have a price"}, 400
        elif "Invalid input" in str_error:
            return {"message": "Invalid input"}, 400
        return {"message": f"Something else went wrong"}, 400


@order_blueprint.route('/cancel', methods=['PUT'])
@api_required
def cancel_order():
    """ 
    :param order_id: id of the order to cancel
    :return: json with the order
    """
    # get api_key from request
    api_key = request.json.get("api_key")
    # get order_uid from query string
    order_id = request.args.get('order_id')
    ticker = request.args.get('ticker')
    try:
        if order_id:
            order = _cancel_order(order_id, api_key)
            if order:
                return jsonify({"message": f"Cancelled the order with: {order_id}"}), 200
            else:
                return jsonify({"message": f"No pending order found on order_id: {ticker}"}), 400
        elif ticker:
            orders = get_orders_pending(ticker)
            if orders:
                for order in orders:
                    _cancel_order(order.id, api_key)
                return jsonify({"message": f"Cancelled all pending orders on ticker: {ticker}"}), 200
            else:
                return jsonify({"message": f"No pending order found on ticker: {ticker}"}), 400
        else:
            return jsonify({"message": "Please enter an order id or ticker to cancel order"}), 400
    except Exception as error:
        return str(error), 400
