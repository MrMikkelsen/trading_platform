from DB.models.mainbase import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from DB.models.orders import Order
from DB.models.holdings import Holding
from DB.models.completed_orders import CompletedOrder


class Security(Base):
    __tablename__ = 'securities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    security_type = Column(String, nullable=False)
    symbol = Column(String, unique=True, nullable=False)

    # one-to-many relationship with holdings table
    holdings = relationship("Holding", back_populates="security")

    # one-to-many relationship with orders table
    orders = relationship("Order", back_populates="security")

    def __init__(self, security_type, symbol):
        self.security_type = security_type
        self.symbol = symbol
