from utils.time_simulator import time_con
from functools import reduce
import datetime
import math


def get_current_portfolio_value(stock_prices_current, holdings):
    current_portfolio_value = 0

    for holding, symbol in holdings:
        current_price = stock_prices_current.get(symbol, 0)
        stocks_in_portfolio = holding.amount

        current_portfolio_value += current_price * stocks_in_portfolio

    return current_portfolio_value


def calculate_statistical_measures(profit_history_offset):
    """
    Calculate statistical measures of the profit history depending on the offset
    return:
        {
            mean : float
            std : float
            std_pl : float
            pl : float
            skewness_pl : float
        }
    """
    profit_history_offset.reverse()
    mean = reduce(lambda a, b: a + b["profit_currency"],
                  profit_history_offset, 0) / len(profit_history_offset) if len(profit_history_offset) != 0 else 0
    std = math.sqrt(reduce(lambda a, b: a + (b["profit_currency"] - mean)
                    ** 2, profit_history_offset, 0) / len(profit_history_offset)) if len(profit_history_offset) != 0 else 0
    std_pl = std if not math.isnan(std) else 0
    pl, skewness_pl = calculate_skewness_pl(profit_history_offset, mean, std)

    return {"mean": mean, "std": std, "std_pl": std_pl, "pl": pl, "skewness_pl": skewness_pl}


def calculate_skewness_pl(profit_history_offset, mean, std):
    profit_history_sort_currency = sorted(
        profit_history_offset, key=lambda x: x["profit_currency"], reverse=True)
    skewness_pl = 0
    pl = profit_history_offset[-1]["profit_currency"] if profit_history_offset and len(
        profit_history_offset) > 0 else 0

    if len(profit_history_sort_currency) > 0:
        middle = len(profit_history_sort_currency) // 2
        median = profit_history_sort_currency[middle]["profit_currency"] if len(profit_history_sort_currency) % 2 != 0 else (
            profit_history_sort_currency[middle - 1]["profit_currency"] + profit_history_sort_currency[middle]["profit_currency"]) / 2
        skewness = 3 * (mean - median) / std if std != 0 else 0
        skewness_pl = skewness if not math.isnan(skewness) else 0
    return pl, skewness_pl
