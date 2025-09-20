import datetime
import uuid
from DB.models.mainbase import Base
from utils.time_simulator import time_con
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields


class Profit_history(Base):
    __tablename__ = 'profit_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    profit_percentage = Column(Float)
    profit_currency = Column(Float)
    saldo = Column(Float)
    position_size = Column(Float)
    date_stamp = Column(DateTime)

    # composite index on team_id and date_stamp
    Index('ix_team_date_stamp', team_id, date_stamp)

    def __init__(self, team_id, profit_percentage, profit_currency, saldo, position_size, date_stamp):
        self.team_id = team_id
        self.profit_percentage = profit_percentage
        self.profit_currency = profit_currency
        self.saldo = saldo
        self.position_size = position_size
        self.date_stamp = date_stamp
