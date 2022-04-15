import configparser
import json

import websocket

from api.models.base_model import BaseModel

config = configparser.ConfigParser()
config.read("api/conf/cfg_test_environment.ini")
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
        ws.send(body)
        response = ws.recv()
        ws.close()
        return response
