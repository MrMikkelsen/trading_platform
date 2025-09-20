'''
This is used for logging additional funds to teams (e.g. good will)
'''
from datetime import datetime
from DB.models.mainbase import Base
from utils.time_simulator import time_con
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, Index, String, Float, ForeignKey, event, DDL
import uuid
from sqlalchemy.orm import relationship


class Goodwill(Base):
    __tablename__ = 'goodwill'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_at_simulated_time = Column(DateTime)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)

    update_team_saldo_trigger = DDL("""
        CREATE OR REPLACE FUNCTION update_team_saldo()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE teams
            SET saldo = saldo + NEW.amount
            WHERE teams.id = NEW.team_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER update_team_saldo
        AFTER INSERT ON goodwill
        FOR EACH ROW
        EXECUTE PROCEDURE update_team_saldo();
    """)

    def __init__(self, team_id, amount):
        self.team_id = team_id
        self.amount = amount
        self.created_at_simulated_time = time_con.get_current_time()


# run the trigger
event.listen(Goodwill.__table__, 'after_create',
             Goodwill.update_team_saldo_trigger.execute_if(dialect='postgresql'))
# if index don't exist, create it
