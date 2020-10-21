from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import SQL_DB

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    lineman_app = Flask(__name__)
    lineman_app.config["SQLALCHEMY_DATABASE_URI"] = SQL_DB

    db.init_app(lineman_app)

    with lineman_app.app_context():
        from resources import Home, StationBarrier

        lineman_api = Api(lineman_app)
        lineman_api.add_resource(Home, "/")
        lineman_api.add_resource(StationBarrier, "/<station_name>")
        db.create_all()

        return lineman_app
