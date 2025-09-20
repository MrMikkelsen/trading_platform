from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SQLALCHEMY_ENGINE_OPTIONS = {
    "echo": False,
    "max_overflow": 100,     # Allow more overflow connections during spikes
    "pool_pre_ping": True,   # Keep this to prevent stale connections
    "pool_recycle": 600,     # Increase to 10 minutes
    "pool_size": 200,        # Much larger pool for your hardware
    "pool_timeout": 30,      # Give a bit more time for connection acquisition
}
# create postgres14 engine with login info from docker-compose

# TODO: Currently identical. But should be different DBs
# TODO: Read from config
engine = create_engine(
    'postgresql://stock:D3nt15t_@postgrelinc.postgres.database.azure.com:5432/postgres', **SQLALCHEMY_ENGINE_OPTIONS)


# OLD implementation
#Session = sessionmaker(engine)

# NEW implementation (see if this works, performance wise)
Session = scoped_session(sessionmaker(bind=engine))


def get_session():
    return Session()
