from flask import Flask
from celery import Celery
from DB.create_db import build_database
from DB.session import db
from DB.models import *
from flask_migrate import Migrate
# ./app/init.py
from controller.historic_controller import data_blueprint
from controller.symbols_controller import symbol_blueprint
from controller.transaction_controller import order_blueprint
from controller.account_controller import account_blueprint
from controller.authorization_controller import authorization_blueprint
from controller.feed_controller import feed_blueprint
import celeryconfig


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://stock:D3nt15t_@postgrelinc.postgres.database.azure.com:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
    app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

    db.init_app(app)
    Migrate(app, db)
    # initializing routes
    app.register_blueprint(symbol_blueprint, url_prefix="/symbols")
    app.register_blueprint(data_blueprint, url_prefix="/data")
    app.register_blueprint(order_blueprint, url_prefix="/order")
    app.register_blueprint(account_blueprint, url_prefix="/account")
    app.register_blueprint(authorization_blueprint, url_prefix="/auth")
    app.register_blueprint(feed_blueprint, url_prefix="/feed")
    with app.app_context():
        build_database()
    return app


app = create_app()
celery = make_celery(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
