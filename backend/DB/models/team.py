from DB.models.mainbase import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Index, String, Float, ForeignKey
import uuid
from sqlalchemy.orm import relationship


def generateUUID():
    return str(uuid.uuid4())


class Team(Base):
    __tablename__ = 'teams'
    #__table_args__ = {'keep_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_key = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String)
    saldo = Column(Float)
    starting_saldo = Column(Float)

    # one-to-many relationship with orders table
    orders = relationship("Order", back_populates="team",
                          cascade="all,delete",
                          lazy='joined')

    holdings = relationship("Holding", back_populates="team",
                            cascade="all,delete",
                            lazy='joined')

    # one-to-many relationship with goodwill table
    goodwills = relationship("Goodwill", backref="team",
                             cascade="all,delete",
                             lazy='joined')

    def __init__(self, name, role, saldo, starting_saldo):
        self.name = name
        self.role = role
        self.saldo = saldo
        self.api_key = generateUUID()
        self.starting_saldo = starting_saldo
