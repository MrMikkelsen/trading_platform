import datetime
from datetime import timedelta
import uuid
from DB.models.mainbase import Base
from utils.time_simulator import time_con
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Index, Integer, Float, DateTime, ForeignKey, DDL, Enum, event, String
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
import sqlalchemy as db
# Define a Marshmallow schema for the Order model


# it is important this is the only thing we expose to the outside world
# because we will make "future" information, that cannot be exposed
class OrderSchema(Schema):
    id = fields.UUID(dump_only=True)
    amount = fields.Integer()
    price = fields.Float()
    order_type = fields.Str()
    order_status = fields.Str()
    created_at = fields.DateTime()
    ended_at = fields.DateTime()
    team_id = fields.UUID()
    security_id = fields.UUID()


class CompletedOrder(Base):
    __tablename__ = 'completed_orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Integer)
    price = Column(Float)
    order_type = Column(
        Enum('buy', 'sell', 'stoploss',
             name='order_type'))
    order_status = Column(
        Enum('pending', 'completed', 'cancelled',
             name='order_status'),
        default='pending', index=True)
    created_at = Column(DateTime)
    ended_at = Column(DateTime)
    cancel_date = Column(DateTime)
    ##### FUTURE INFORMATION #####
    future_striking_price = Column(Float)
    future_striking_date = Column(DateTime)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    security_id = Column(UUID(as_uuid=True), ForeignKey(
        'securities.id'), index=True)

    # create composite index on team_id and order_status
    Index('ix2_team_date', team_id, created_at, ended_at)

    Index('ix_3rd_orders', team_id, security_id, order_type)

    check_completed_order_safety_function = DDL("""
    CREATE OR REPLACE FUNCTION check_completed_order_safety_func(NEW completed_orders)
    RETURNS VOID AS $$
    BEGIN
        IF NEW.order_type = 'buy' THEN
            IF NEW.amount * NEW.price > (SELECT saldo FROM teams WHERE id = NEW.team_id) THEN
                RAISE EXCEPTION 'Not enough saldo to buy';
            END IF;
        ELSIF NEW.order_type = 'sell' THEN
            IF NOT EXISTS (SELECT 1 FROM holdings WHERE team_id = NEW.team_id AND security_id = NEW.security_id AND amount >= NEW.amount) THEN
                RAISE EXCEPTION 'Not enough stock to sell';
            END IF;
        ELSIF NEW.order_type = 'stoploss' THEN
            IF NOT EXISTS (SELECT 1 FROM holdings WHERE team_id = NEW.team_id AND security_id = NEW.security_id AND amount >= NEW.amount) THEN
                RAISE EXCEPTION 'Not enough stock to set stoploss';
            END IF;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)

    process_completed_order_function = DDL("""
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE OR REPLACE FUNCTION process_completed_order_func(NEW completed_orders)
    RETURNS VOID AS $$
    BEGIN
        -- Cancel all pending orders of the same type
        DELETE FROM orders
            WHERE team_id = NEW.team_id
                AND security_id = NEW.security_id
                AND order_type = NEW.order_type
                AND order_status = 'pending'
                OR order_status = 'cancelled'
                AND id != NEW.id;

        IF NEW.order_type = 'buy' THEN
            -- Update team's saldo
            UPDATE teams SET saldo = saldo - (NEW.price * NEW.amount) WHERE id = NEW.team_id;

            -- Update holdings
            INSERT INTO holdings (id, team_id, security_id, amount)
            VALUES (uuid_generate_v4(), NEW.team_id,
                    NEW.security_id, NEW.amount)
            ON CONFLICT (team_id, security_id)
            DO UPDATE SET amount = holdings.amount + EXCLUDED.amount;
        ELSIF NEW.order_type = 'sell' OR NEW.order_type = 'stoploss' THEN
            -- Update team's saldo
            -- Update holdings
            UPDATE holdings SET amount = amount - NEW.amount WHERE team_id = NEW.team_id AND security_id = NEW.security_id;

            UPDATE teams SET saldo = saldo + (NEW.price * NEW.amount) WHERE id = NEW.team_id;

        END IF;

    END;
    $$ LANGUAGE plpgsql;
    """)

    process_completed_order_on_insert_trigger = DDL("""
        CREATE OR REPLACE FUNCTION process_completed_order_on_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Check if the order is safe
            PERFORM check_completed_order_safety_func(NEW);

            -- If order status is completed, process the order
            PERFORM process_completed_order_func(NEW);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER process_completed_order_on_insert_trigger
        BEFORE INSERT ON completed_orders
        FOR EACH ROW
        EXECUTE PROCEDURE process_completed_order_on_insert();
    """)

    def __init__(self, team_id, security_id, amount, price, order_type, created_at):
        self.team_id = team_id
        self.security_id = security_id
        self.amount = amount
        self.price = price
        self.order_type = order_type
        self.created_at = created_at


# Functions
event.listen(CompletedOrder.__table__, 'after_create',
             CompletedOrder.process_completed_order_function)
event.listen(CompletedOrder.__table__, 'after_create',
             CompletedOrder.check_completed_order_safety_function)

# Triggers
event.listen(CompletedOrder.__table__, 'after_create',
             CompletedOrder.process_completed_order_on_insert_trigger)
