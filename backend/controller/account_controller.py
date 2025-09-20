from DB.models.team import Team
from utils.security import admin_required
from utils.security import api_required
from DB.functions.orders import get_all_pending_orders, get_all_completed_orders, get_all_stoploss_orders
from DB.functions.teams import get_team_saldo, get_team_id, add_additional_funds, get_team_holdings
from flask import request, Blueprint

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/saldo', methods=['GET'])
@api_required
def get_saldo(team: Team):
    '''
    :return: saldo for team'''
    saldo = get_team_saldo(team.id)

    # return float saldo with 2 decimals as json with key saldo
    return {"saldo": round(saldo, 2)}, 200


@account_blueprint.route('/portfolio', methods=['GET'])
@api_required
def get_portfolio(team: Team):
    '''
    :return: portfolio for team'''
    portfolio = get_team_holdings(team.id)
    return portfolio, 200


@account_blueprint.route('/open_orders', methods=['GET'])
@api_required
def get_open_orders(team: Team):
    '''
    :return: open orders for team'''
    orders = get_all_pending_orders(team.id)
    return orders, 200


@account_blueprint.route('/get_completed_orders', methods=['GET'])
@api_required
def get_completed_orders(team: Team):
    '''
    :return: completed orders for team'''
    api_key = request.json.get("api_key")
    team_id = get_team_id(api_key)
    orders = get_all_completed_orders(team_id)
    return orders, 200


@account_blueprint.route('/get_stoploss_orders', methods=['GET'])
@api_required
def get_stoploss_orders(team: Team):
    """
    :return: stop loss orders for team
    """
    try:
        stoploss_orders = get_all_stoploss_orders(team.id)
        return stoploss_orders, 200
    except Exception as error:
        return str(error), 400


@account_blueprint.route('/add_goodwill/<team_api_key>/<amount>', methods=['POST'])
@api_required
@admin_required
def add_goodwill(team, team_api_key, amount):
    '''
    :param team_id: id of the team
    :param amount: amount to add
    :return: saldo for team'''
    try:
        team_id = get_team_id(team_api_key)
        add_additional_funds(team_id, amount)
        return {"message": f"goodwil added, amount: {amount}"}, 200
    except Exception as error:
        return str(error), 400
