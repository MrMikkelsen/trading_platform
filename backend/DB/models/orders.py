import datetime
from datetime import timedelta
import uuid
from DB.models.mainbase import Base
from utils.time_simulator import time_con
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Index, Integer, Float, DateTime, ForeignKey, DDL, Enum, event
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


class Order(Base):
    __tablename__ = 'orders'

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
    Index('ix_team_order_status', team_id, order_status)

    Index('ix_team_security_order_status_type', team_id,
          security_id, order_type, order_status)

    Index('ix_pending_orders', team_id, security_id, order_type,
          postgresql_where=order_status == 'pending')

    # many-to-one relationship with teams table
    team = relationship("Team", back_populates="orders", lazy='joined')

    # many-to-one relationship with securities table
    security = relationship("Security", back_populates="orders", lazy='joined')

    check_order_safety_function = DDL("""
    CREATE OR REPLACE FUNCTION check_order_safety_func(NEW orders)
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

    process_order_function = DDL("""
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE OR REPLACE FUNCTION process_order_func(NEW orders)
    RETURNS VOID AS $$
    BEGIN
        -- Insert order into completed_orders table
        INSERT INTO completed_orders SELECT * FROM orders WHERE id = NEW.id;

        -- Delete order from orders table
        DELETE FROM orders WHERE id = NEW.id;

    END;
    $$ LANGUAGE plpgsql;
    """)

    # Trigger to process order on insert
    process_order_on_insert_trigger = DDL("""
        CREATE OR REPLACE FUNCTION process_order_on_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Check if the order is safe
            PERFORM check_order_safety_func(NEW);

            -- Cancel any existing orders for the same security, team and order type
            DELETE FROM orders
            WHERE team_id = NEW.team_id
                AND security_id = NEW.security_id
                AND order_type = NEW.order_type
                AND order_status = 'pending'
                OR order_status = 'cancelled'
                AND id != NEW.id;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER process_order_on_insert_trigger
        BEFORE INSERT ON orders
        FOR EACH ROW
        EXECUTE PROCEDURE process_order_on_insert();
    """)

    # Trigger to process order on update
    process_order_on_update_trigger = DDL("""
        CREATE OR REPLACE FUNCTION process_order_on_update()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Check if the order status has been updated to completed
            IF OLD.order_status = 'pending' AND NEW.order_status = 'completed' THEN

                -- Process the order
                PERFORM process_order_func(NEW);
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER process_order_on_update_trigger
        AFTER UPDATE ON orders
        FOR EACH ROW
        EXECUTE PROCEDURE process_order_on_update();
    """)

    # https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance

    def __init__(self, team_id, security_id, amount, price, order_type, created_at, days_till_cancel):
        self.team_id = team_id
        self.security_id = security_id
        self.amount = amount
        self.price = price
        self.order_type = order_type
        self.created_at = created_at
        self.cancel_date = created_at + timedelta(days=days_till_cancel)


# Functions
event.listen(Order.__table__, 'after_create', Order.process_order_function)
event.listen(Order.__table__, 'after_create',
             Order.check_order_safety_function)
# Triggers
event.listen(Order.__table__, 'after_create',
             Order.process_order_on_insert_trigger)
event.listen(Order.__table__, 'after_create',
             Order.process_order_on_update_trigger)
