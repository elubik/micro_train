import os
from datetime import datetime
from flask_restful import Resource, Api, reqparse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

lineman_app = Flask(__name__)
lineman_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(lineman_app)
lineman_api = Api(lineman_app)

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5002)


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    barrier_state = db.Column(db.String(10), unique=False, nullable=False)
    last_update = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Station %r>' % self.name


db.create_all()


def save_barrier_state(name, state):
    try:
        station_check_0 = db.session.query(Station).filter_by(name=name).first()
        if station_check_0:
            station = db.session.query(Station).filter_by(name=name).update({"barrier_state": state})
        else:
            station = db.session.add(Station(name=name, barrier_state=state))
        db.session.commit()

        return station
    except exc.SQLAlchemyError as err:
        raise err


def get_barrier_state(name):
    try:
        return db.session.query(Station).filter_by(name=name).first()
    except exc.SQLAlchemyError as err:
        raise err


class StationBarrier(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.barrier_state = 'barrier_state'

    def put(self, station_name):
        self.parser.add_argument(self.barrier_state)
        barrier_state = self.parser.parse_args().get(self.barrier_state)
        if barrier_state:
            task = save_barrier_state(station_name, barrier_state)
            return {'Response': 'OK'}
        else:
            return {'Response': 'ERROR',
                    'Message': 'Incorrect param'}

    def get(self, station_name):
        if station_name:
            station = get_barrier_state(station_name)
            if station:
                return {'Response': 'OK',
                        'Message': {
                            'station_name': station.name,
                            'barrier_state': station.barrier_state,
                            'last_update': str(station.last_update)
                        }}
            else:
                return {'Response': 'OK',
                        'Message': {'empty': 'No record'}}
        else:
            return {'Response': 'ERROR',
                    'Message': 'Incorrect param'}


class Home(Resource):
    def get(self):
        return {'Response': 'OK',
                'Message': "Please type in station name in url after '/', like http://localhost:5002/Białystok"}


lineman_api.add_resource(StationBarrier, '/<station_name>')
lineman_api.add_resource(Home, '/')

if __name__ == '__main__':
    lineman_app.run(port=str(PORT), debug=True)
