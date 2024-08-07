from flask_restful import Resource, reqparse

from models import Station
from api import db


def save_barrier_state(name: str, state: str) -> None:
    try:
        station_check_0 = db.session.query(Station).filter_by(name=name).first()
        if station_check_0:
            db.session.query(Station).filter_by(name=name).update(
                {"barrier_state": state}
            )
        else:
            db.session.add(Station(name=name, barrier_state=state))
        db.session.commit()

    except Exception as ex:
        raise Exception(ex)
    finally:
        db.session.close()


def get_barrier_state(name: str) -> db.session.query:
    try:
        return db.session.query(Station).filter_by(name=name).first()
    except Exception as ex:
        raise Exception(ex)
    finally:
        db.session.close()


class StationBarrier(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.barrier_state = "barrier_state"

    def put(self, station_name: str) -> dict:
        self.parser.add_argument(self.barrier_state)
        barrier_state = self.parser.parse_args().get(self.barrier_state)
        if barrier_state:
            save_barrier_state(station_name, barrier_state)
            return {"Response": "OK"}
        else:
            return {"Response": "ERROR", "Message": "Incorrect param"}

    def get(self, station_name: str) -> dict:
        if station_name:
            station = get_barrier_state(station_name)
            if station:
                return {
                    "Response": "OK",
                    "Message": {
                        "station_name": station.name,
                        "barrier_state": station.barrier_state,
                        "last_update": str(station.last_update),
                    },
                }
            else:
                return {"Response": "OK", "Message": {"empty": "No record"}}
        else:
            return {"Response": "ERROR", "Message": "Incorrect param"}


class Home(Resource):
    def get(self) -> dict:
        return {
            "Response": "OK",
            "Message": "Please type in station name in url after '/', like http://localhost:5002/Białystok",
        }
