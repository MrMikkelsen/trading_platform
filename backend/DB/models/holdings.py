from DB.models.mainbase import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
import uuid
from sqlalchemy.orm import relationship


class Holding(Base):
    __tablename__ = 'holdings'
    # __table_args__ = {'keep_existing': True}
    # join table for many to many relationship between team and stock
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    security_id = Column(UUID(as_uuid=True), ForeignKey('securities.id'))

    amount = Column(Integer)

    # relationships
    team = relationship("Team", back_populates="holdings")
    security = relationship("Security", back_populates="holdings")

    __table_args__ = (UniqueConstraint(
        'team_id', 'security_id', name='_team_security_uc'),)

    # composite index on team_id and security_id
    Index('ix_team_security', team_id, security_id)

    def __init__(self, amount, team_id, security_id):
        self.amount = amount
        self.team_id = team_id
        self.security_id = security_id
