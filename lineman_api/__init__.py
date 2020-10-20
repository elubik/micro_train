from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from lineman_api.config import sql_db

lineman_app = Flask(__name__)
lineman_app.config['SQLALCHEMY_DATABASE_URI'] = sql_db
db = SQLAlchemy(lineman_app)
lineman_api = Api(lineman_app)
db.create_all()
