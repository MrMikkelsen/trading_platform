from utils.security import api_required
from utils.exchange import prices_con
from utils.time_simulator import time_con
from flask import jsonify, Blueprint, request
import sys

data_blueprint = Blueprint('data', __name__)

ONE_YEAR = 365


@data_blueprint.route('', methods=['GET'])
@api_required
def get_historic_data():
    '''
    :param ticker: ticker to get prices for
    :param days_back: number of days back to get prices for
    :return: prices for ticker for the last days_back days'''
    # get query params
    ticker = request.args.get('ticker')
    days_back = request.args.get('days_back')

    if ticker is not None:
        try:
            ticker = ticker.upper().strip()
        except ValueError:
            return jsonify({"error": "Invalid ticker"}), 400
    if days_back is not None:
        try:
            days_back = int(days_back)
            if days_back < 0 or days_back > ONE_YEAR:
                return jsonify({"error": "Invalid days back"}), 400
        except ValueError:
            return jsonify({"error": "Invalid days back"}), 400

    prices = prices_con.prices_for_ticker(ticker=ticker, days_back=days_back)
    return jsonify(prices), 200


@data_blueprint.route('/stocks', methods=["GET"])
def current_price_time():
    """
    :return: current price for all tickers
    """
    ticker = request.args.get('ticker')
    current_prices = prices_con.get_current_price(ticker)
    return jsonify({"data": current_prices}), 200
