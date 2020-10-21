import requests
from flask import Flask
from resources import save_barrier_state, get_barrier_state
from config import HOST, PORT

from models import Station
from api import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
db.init_app(app)


class TestDatabase:
    def test_save_barrier_state(self):
        with app.app_context():
            db.create_all()
            station_name = "Białystok"
            barrier_state = "down"
            save_barrier_state(station_name, barrier_state)
            station_check = db.session.query(Station).filter_by(name=station_name).first()
            assert station_check.name == station_name
            assert station_check.barrier_state == barrier_state

    def test_get_barrier_state(self):
        with app.app_context():
            db.create_all()
            station_name = "Białystok"
            result = get_barrier_state(station_name)
            assert result


class TestApi:
    def test_barrier_get_home_url(self):
        response = requests.get(f'http://{HOST}:{PORT}/')
        assert response.status_code == 200
        assert response.json().get('Response') == 'OK'
        assert True

    def test_barrier_get(self):
        response = requests.get(f'http://{HOST}:{PORT}/Białystok')
        assert response.status_code == 200
        assert response.json().get('Response') == 'OK'
        assert True

    def test_barrier_down(self):
        response = requests.put(f'http://{HOST}:{PORT}/Warszawa', data={'barrier_state': 'down'})
        assert response.json().get('Response') == 'OK'

    def test_barrier_up(self):
        response = requests.put(f'http://{HOST}:{PORT}/Łowicz', data={'barrier_state': 'up'})
        assert response.json().get('Response') == 'OK'
