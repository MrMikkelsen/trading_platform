
import uuid
from DB.models.holdings import Holding
from DB.models.securities import Security
from DB.models.team import Team
from DB.models.goodwill import Goodwill
from DB.models.profit_history import Profit_history
from DB.functions.orders import get_average_traded_price, get_all_completed_orders, get_volume_completed_orders_history, get_all_pending_orders, get_trade_history_unique_trades_offset, get_avg_length_of_trade, get_all_stoploss_orders
from DB.session import get_session
from utils.exchange import prices_con
from utils.time_simulator import time_con
from utils.calc import calculate_statistical_measures
from sqlalchemy import desc, asc
from collections import defaultdict
import datetime
from sqlalchemy import MetaData
from DB.session import get_session


def get_team_id(api_key: str) -> int:
    """Get the team id of a team"""
    with get_session() as session:
        team = session.query(Team).filter(Team.api_key == api_key).first()
        return team.id


def get_team(api_key: str) -> Team:
    """Get the team of a team"""
    with get_session() as session:
        team = session.query(Team).filter(Team.api_key == api_key).first()
        return team


def get_team_name(api_key: str) -> str:
    """Get team name of a team with api_key as input"""
    with get_session() as session:
        team = session.query(Team).filter(Team.api_key == api_key).first()
        return team.name


def get_all_team_ids() -> list:
    with get_session() as session:
        result = session.query(Team.id).filter(Team.role == "group").all()
        return [team_id[0] for team_id in result]


def get_all_team_tokens() -> list:
    with get_session() as session:
        result = session.query(Team.api_key).filter(Team.role == "group").all()
        return [team_api_key[0] for team_api_key in result]


def get_team_login(api_key: str) -> dict:
    """Get necessary information for authorization"""
    with get_session() as session:
        team = session.query(Team).filter(Team.api_key == api_key).first()
        return {"role": team.role, "name": team.name, "token": team.api_key}


def add_additional_funds(team_id, amount):
    """Add additional funds to a team"""
    with get_session() as session:
        try:
            team_id = str(team_id)
            amount = float(amount)
        except:
            raise Exception("Invalid input")

        team = session.query(Team).filter(Team.id == team_id).first()
        if team is None:
            raise Exception("Team does not exist")

        try:
            goodwill = Goodwill(
                team_id=team_id, amount=amount)
            session.add(goodwill)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Could not add goodwill")


def get_team_goodwill(team_id: int) -> float:
    """Get goodwill of the team"""
    with get_session() as session:
        amount = session.query(Goodwill.amount).filter(
            team_id == Goodwill.id).first()
        if amount is None:
            return 0
        else:
            return amount


def get_team_saldo(team_id: int) -> float:
    """Get the saldo of a team"""
    with get_session() as session:
        team = session.query(Team).filter(Team.id == team_id).first()
        return team.saldo


def get_team_start_saldo(team_id: int) -> float:
    """Get the starting saldo of a team"""
    with get_session() as session:
        team = session.query(Team).filter(Team.id == team_id).first()
        return team.starting_saldo


def get_team_holdings(team_id: int):
    "Return Securitys held and the symbol"
    with get_session() as session:
        holdings = session.query(Holding, Security.symbol).filter(Holding.team_id == team_id).join(
            Security, Holding.security_id == Security.id).order_by(Security.symbol).all()
        portfolio_dict = {
            symbol: holding.amount for holding, symbol in holdings}
        return portfolio_dict


def get_team_portfolio(team_id: int, stocks_average_traded_price, holdings) -> list:
    """Get the portfolio of a team"""
    # get all stocks where id == holding.stock_id
    portfolio = []
    # iterate over stocks_trading_history, getting symbol (key) and the values from the dict in the value

    for symbol, avg_price in stocks_average_traded_price.items():
        stocks_in_portfolio = holdings.get(symbol, 0)
        # Get yesterdays price and current price
        open_price = prices_con.get_opening_price_for_ticker(symbol)
        current_price = prices_con.get_current_price_for_ticker(symbol)

        if open_price != 0:
            try:
                diff_day = round((
                    current_price - open_price) / open_price * 100, 2)
            except Exception as e:
                print("\033[91m" +
                      f"Error in get_team_portfolio. {e}" + "\033[0m")
                diff_day = 0

        since_purchase = (current_price - avg_price) * \
            stocks_in_portfolio if stocks_in_portfolio > 0 and current_price != 0 else None
        since_purchase_percentage = round(
            (current_price - avg_price) / avg_price * 100, 2) if since_purchase is not None else None

        current_value_of_stock = stocks_in_portfolio * current_price
        # add the difference if it was calculated otherwise none
        portfolio.append({
            'symbol': symbol,
            'amount': stocks_in_portfolio,
            'currentValue': current_value_of_stock,
            'diff_day': diff_day if diff_day else None,
            'since_purchase': since_purchase,
            'since_purchase_percentage': since_purchase_percentage
        })

    portfolio = sorted(portfolio, key=lambda x: x['symbol'])
    return portfolio


def get_group_data_one_group_adminpage(token, offset=0):
    '''
    :return: payload of all the data needed for frontend AdminPage presentation
    '''
    team = get_team(token)

    volume_trading_history = get_volume_completed_orders_history(
        team.id, offset)

    total_goodwill_amount = sum(
        goodwill.amount for goodwill in team.goodwills)

    profit_history = get_group_profit_history(team.id, offset)
    # Profit_history list is reversed in calculate statistical measure to fulfill frontend needs, kind of weird so I leave a comment here
    # TODO: fix this ^ but no time for it right now

    statisical_measures = calculate_statistical_measures(profit_history)

    unique_trades = get_trade_history_unique_trades_offset(team.id, offset)

    average_trading_length = get_avg_length_of_trade(team.id, offset)

    group_standing = {
        "name": team.name,
        "token": token,
        "uniqueTrades": unique_trades,
        "avgTradeLength": average_trading_length,
        "stdPL": statisical_measures["std_pl"],
        "PL": statisical_measures["pl"],
        "skewnessPL": statisical_measures["skewness_pl"],
        "data": {"balance": team.saldo, "numberOfStocks": volume_trading_history["numberOfStocks"], "numberOfTrades": volume_trading_history["numberOfTrades"], "goodwill": total_goodwill_amount},
    }
    # return float saldo with 2 decimals as json with key saldo

    return group_standing


# TODO: This function should probably be located in DB.functions.teams.py
def get_group_data_one_group(token, offset=0):
    '''
    :return: payload of all the data needed for frontend presentation
    '''
    team = get_team(token)
    stocks_average_traded_price = get_average_traded_price(team.id, offset)

    volume_trading_history = get_volume_completed_orders_history(
        team.id, offset)

    holdings = get_team_holdings(team.id)

    portfolio = get_team_portfolio(
        team.id, stocks_average_traded_price, holdings)

    past_transactions = get_all_completed_orders(team.id)

    pending_transactions = get_all_pending_orders(team.id)

    current_portfolio_value = sum(
        stock['currentValue'] for stock in portfolio)

    total_goodwill_amount = sum(
        goodwill.amount for goodwill in team.goodwills)

    profit_loss = (team.saldo + current_portfolio_value) \
        - (team.starting_saldo + total_goodwill_amount)

    profit_history = get_group_profit_history(team.id, offset)
    # Profit_history list is reversed in calculate statistical measure to fulfill frontend needs, kind of weird so I leave a comment here
    # TODO: fix this ^ but no time for it right now

    stop_losses = get_all_stoploss_orders(team.id)

    group_standing = {
        "name": team.name,
        "token": token,
        "stocks": portfolio,
        "portfolio": portfolio,
        "orders": pending_transactions,
        "stopLosses": stop_losses,
        "profit_history": profit_history,
        "pastSales": past_transactions,
        "data": {"balance": team.saldo, "numberOfStocks": volume_trading_history["numberOfStocks"], "profit": profit_loss, "current_portfolio_value": current_portfolio_value, "numberOfTrades": volume_trading_history["numberOfTrades"]},
    }

    return group_standing


def get_group_profit_history(team_id: int, offset: int):

    with get_session() as session:
        if offset == 0:
            profit_history = session.query(Profit_history).filter(
                Profit_history.team_id == team_id).order_by(desc(Profit_history.date_stamp)).all()
        else:
            current_time = time_con.get_current_time()
            date_now = current_time.replace(
                hour=0, minute=0, second=0, microsecond=0)
            date_offset = date_now - datetime.timedelta(days=offset)

            profit_history = session.query(Profit_history).filter(
                Profit_history.team_id == team_id).filter(
                Profit_history.date_stamp >= date_offset).filter(Profit_history.date_stamp <= date_now).order_by(desc(Profit_history.date_stamp)).all()
        return [
            {
                "profit_percentage": profit.profit_percentage,
                "profit_currency": profit.profit_currency,
                "gmtTime": profit.date_stamp
            } for profit in profit_history
        ]


def all_group_update_profit_history(date_stamp):
    with get_session() as session:
        # get all teams, Team where role == 'team'
        teams = session.query(Team).filter(Team.role == 'group').all()
        for team in teams:
            total_current_portfolio_value = sum(
                [holding.amount * prices_con.get_current_price_for_ticker(holding.security.symbol)
                 for holding in team.holdings])

            total_goodwill_amount = sum(
                goodwill.amount for goodwill in team.goodwills)

            total_profit = (team.saldo + total_current_portfolio_value) \
                - (team.starting_saldo + total_goodwill_amount)

            total_profit_percentage = round(
                total_profit / (team.starting_saldo + total_goodwill_amount) * 100, 2)

            profit_history = Profit_history(
                team_id=team.id,
                profit_percentage=total_profit_percentage,
                profit_currency=total_profit,
                date_stamp=date_stamp,
                saldo=team.saldo,
                position_size=total_current_portfolio_value,
            )
            session.add(profit_history)
            session.commit()


def get_all_teams_cumulative_data():
    with get_session() as session:

        # query the profit_percentage, date_stamp, and name of all teams
        profit_history = session.query(Profit_history.profit_percentage, Profit_history.date_stamp, Team.name)\
            .join(Team, Team.id == Profit_history.team_id)\
            .order_by(asc(Profit_history.date_stamp))

        # create a dictionary to store the data for each team
        data = defaultdict(lambda: defaultdict(int))
        labels = set()

        for profit, date, team_name in profit_history:
            labels.add(date)
            data[team_name][date] = profit

        # sort the labels
        labels = sorted(list(labels))

        # format the data for each team
        for team_name in data.keys():
            team_data = []
            for label in labels:
                if label in data[team_name]:
                    team_data.append(data[team_name][label])
                else:
                    pass  # Don't add if there is no data
            data[team_name] = team_data

        return {
            'labels': labels,
            'data': data
        }


def get_and_collect_all_group_data(offset=0):
    # TODO: error handling
    data = []

    # TODO: this function needs to change!
    team_tokens = get_all_team_tokens()
    for token in team_tokens:
        group_data = get_group_data_one_group_adminpage(
            token, offset=offset)
        if group_data:
            data.append(group_data)

    return data
