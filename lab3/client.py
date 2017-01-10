import requests, json

from base_client import BaseClient


class Client(BaseClient):
    BASE_URL = 'https://api.vk.com/method/'
    user_name = ''
    user_id = ''
    payload = {}

    def __init__(self, user_name):
        self.user_name = user_name
        self.payload = {'v': '5.57', 'user_ids': self.user_name}
        self.user_id = self.get_id()

    def get_id(self):
        resp = self._get_data('users.get', self.payload)
        return resp['response'][0]['id']

    def _get_data(self, method, param):
        response = requests.get(self.generate_url(method), params=param)
        response = response.json()
        # print(response)
        return self.response_handler(response)

    def response_handler(self, response):
        if 'error' not in response:
            return response
        else:
            raise NameError

    def execute(self):
        return self.user_id
