from lineman_api.app import HOST, PORT
# from time import sleep
import requests


class TestLineman:
    def test_invalid_param(self):
        response = requests.post(f'http://{HOST}:{PORT}/barrier', data={'action': 'go away'})
        assert response.json().get('Response') == 'ERROR'

    def test_barrier_up(self):
        response = requests.post(f'http://{HOST}:{PORT}/barrier', data={'action': 'up'})
        assert response.json().get('Response') == 'OK'

    def test_barrier_down(self):
        response = requests.post(f'http://{HOST}:{PORT}/barrier', data={'action': 'down'})
        assert response.json().get('Response') == 'OK'

    def test_barrier_status_get(self):
        response = requests.get(f'http://{HOST}:{PORT}/barrier', params='task_id')
        assert response.json().get('Response') == 'OK'
