import configparser
import json
import os

import allure
import websocket

from api.models.base_model import BaseModel

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "cfg_test_environment.ini"))
ADDRESS = config['WS']['address']


class TesterClient:

    @classmethod
    def post_to_ws(cls, body):
        ws = websocket.WebSocket()
        ws.connect(ADDRESS)
        if not isinstance(body, str):
            if isinstance(body, BaseModel):
                body = json.dumps(body.dict())
            else:
                body = json.loads(json.dumps(json.dumps(body, default=lambda x: x.__dict__)))

        with allure.step(f'send request to: {ADDRESS}'):
            allure.attach("body", body)
            ws.send(body)

        with allure.step(f'get response'):
            response = ws.recv()
            allure.attach("response", response)
        ws.close()
        return response
