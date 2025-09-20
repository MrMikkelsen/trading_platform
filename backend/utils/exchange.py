from typing import Tuple
from DB.models.orders import Order
from DB.models.securities import Security
from DB.session import get_session
from utils.time_simulator import time_con
import pandas as pd
import numpy as np
import datetime as dt
from functools import lru_cache
import os
import sqlite3
import datetime as dt
from functools import lru_cache
import os
from DB.models.orders import Order
from DB.session import get_session


def setup_db():
    # get path to this file
    path = os.path.dirname(os.path.abspath(__file__))
    sqlite3.enable_callback_tracebacks(True)
    # create connection
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    # create prices table
    conn.execute("CREATE TABLE prices (symbol text, gmtTime text, askMedian real, bidMedian real, askVolume real, bidVolume real, spreadMedian real)")

    # read prices data from CSV file
    prices_data = pd.read_csv(f"{path}/databases/stockPrices_hourly.csv")

    # convert gmtTime column to datetime objects
    prices_data["gmtTime"] = pd.to_datetime(prices_data["gmtTime"])

    # insert data into prices table
    prices_data.to_sql("prices", conn, if_exists="append", index=False)

    # create two indexes on (symbol, askMedian, gmtTime) and (symbol, bidMedian, gmtTime)
    conn.execute(
        "CREATE INDEX index_ask_median ON prices (symbol, askMedian, gmtTime)")
    conn.execute(
        "CREATE INDEX index_bid_median ON prices (symbol, bidMedian, gmtTime)")

    # Create index on just gmtTime
    conn.execute("CREATE INDEX index_gmtTime ON prices (gmtTime)")
    # create index on gmtTime and symbol
    conn.execute(
        "CREATE INDEX index_gmtTime_symbol ON prices (gmtTime, symbol)")

    conn.commit()
    # Make the connection read-only and multithreaded
    conn.execute("PRAGMA query_only = 1;")
    conn.execute("PRAGMA journal_mode = MEMORY;")

    # Set the isolation level of the connection
    conn.isolation_level = None

    return conn


class Exchange:
    """In memory prices"""
    # TODO: Refactor price for ticker and price for all tickers to one method

    def __init__(self):
        self.conn = setup_db()
        self.symbols = self._flatten(self.conn.cursor().execute(
            "SELECT DISTINCT symbol FROM prices").fetchall())

    def prices_for_ticker(self, ticker: str = None, days_back: int = None, rounded_format=False) -> list:
        """Get prices for all tickers"""
        current_time = time_con.get_current_time()
        if days_back is None:
            # start_time is beginning of day of current time
            start_time = dt.datetime(current_time.year,
                                     current_time.month,
                                     current_time.day, 0, 0, 0)
        else:
            start_time = current_time - dt.timedelta(days=days_back)

        # build WHERE clause for SQL query
        query = "SELECT * FROM prices WHERE gmtTime >= ? AND gmtTime <= ?"
        params = (start_time, current_time)
        if ticker is not None and ticker in self.symbols:
            query += " AND symbol = ?"
            params = params + (ticker, )

        # execute query
        cursor = self.conn.cursor().execute(query, params)
        results = cursor.fetchall()
        # return results as list of dictionaries
        if rounded_format:
            result = [{
                "symbol": row[0],
                "gmtTime": row[1],
                "askMedian": round(row[2], 2),
                "bidMedian": round(row[3], 2),
                "askVolume": row[4],
                "bidVolume": row[5],
                "spreadMedian": row[6]
            } for row in results]
        else:
            result = [dict(zip(["symbol", "gmtTime", "askMedian", "bidMedian",
                           "askVolume", "bidVolume", "spreadMedian"], row)) for row in results]

        return result

    def datetime_for_price(self, session, order: Order) -> Tuple[dt.datetime, float]:
        """Get datetime for price"""

        security = session.query(Security).filter_by(
            id=order.security_id).first()
        price = order.price
        start_date = order.created_at
        if order.order_type == "buy" or order.order_type == "stoploss":
            query = "SELECT gmtTime, askMedian FROM prices WHERE symbol = ? AND \
                gmtTime >= ? AND askMedian <= ? ORDER BY gmtTime ASC LIMIT 1"
        else:
            query = "SELECT gmtTime, bidMedian FROM prices WHERE symbol = ? AND \
                gmtTime >= ? AND bidMedian >= ? ORDER BY gmtTime ASC LIMIT 1"

        params = (security.symbol, start_date, price)

        result = self.conn.cursor().execute(query, params).fetchone()
        # if result is not a tuple
        if not isinstance(result, tuple):
            return None, None
        else:
            date, price = result
            return date, price

    def get_all_symbols(self) -> list:
        return self.symbols

    def _flatten(self, l) -> list:
        return [item for sublist in l for item in sublist]

    def get_current_price(self, symbol: str = None) -> dict:
        """
        Get current price for a symbol, i.e., the last price in the database
        If no symbol is provided, return the current price for all symbols
        """
        current_time = time_con.get_current_time()

        if symbol is not None:
            query = """
                    SELECT *
                    FROM prices
                    WHERE symbol = ?
                    AND gmtTime <= ?
                    ORDER BY gmtTime DESC
                    LIMIT 1
                """
            params = (symbol, current_time, current_time)
        else:
            query = f"""
                SELECT prices.symbol, prices.gmtTime, prices.askMedian, prices.bidMedian, prices.askVolume, prices.bidVolume, prices.spreadMedian
                FROM prices
                INNER JOIN (
                    SELECT symbol, MAX(gmtTime) AS max_gmtTime
                    FROM prices
                    WHERE gmtTime <= ?
                    GROUP BY symbol
                ) grouped_prices ON prices.symbol = grouped_prices.symbol AND prices.gmtTime = grouped_prices.max_gmtTime
            """
            params = (current_time,)

        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()

        # return the closest price to current time for each symbol
        return [{
                "symbol": row[0],
                "gmtTime": row[1],
                "askMedian": round(row[2], 2),
                "bidMedian": round(row[3], 2),
                "askVolume": row[4],
                "bidVolume": row[5],
                "spreadMedian": row[6]
                } for row in rows]

    def get_current_price_for_ticker(self, symbol: str) -> dict:
        '''
        get current price for a symbol, i.e., the last price in the database
        the price is an average of the ask and bid prices
        '''

        current_time = time_con.get_current_time()
        query = "SELECT * FROM prices WHERE gmtTime <= ? AND symbol = ? ORDER BY gmtTime DESC LIMIT 1"
        params = (current_time, symbol)
        cursor = self.conn.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return (row[2] + row[3]) / 2

    def get_opening_price_for_ticker(self, symbol: str) -> float:
        """
        Get opening price for a symbol, i.e., the first price for the current day
        The price is an average of the ask and bid prices
        """
        current_time = time_con.get_current_time()
        start_time = dt.datetime(current_time.year,
                                 current_time.month,
                                 current_time.day, 0, 0, 0)

        query = "SELECT * FROM prices WHERE gmtTime >= ? AND gmtTime <= ? AND symbol = ? ORDER BY gmtTime ASC LIMIT 1"
        params = (start_time, current_time, symbol)
        cursor = self.conn.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return (row[2] + row[3]) / 2


prices_con = Exchange()




