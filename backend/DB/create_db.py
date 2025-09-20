
from DB.models.mainbase import Base
from DB.session import engine
import os
from time import sleep
from DB.models.holdings import Holding
from DB.models.goodwill import Goodwill
from DB.models.orders import Order
from DB.models.profit_history import Profit_history
from DB.models.securities import Security
from DB.models.team import Team
from DB.models.completed_orders import CompletedOrder
from sqlalchemy import Index, text
from DB.session import get_session


def build_database():
    # create tables
    Base.metadata.create_all(engine, checkfirst=True)
