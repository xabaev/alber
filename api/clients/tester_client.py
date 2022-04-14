import json

import websocket

from api.models.base_model import BaseModel


class TesterClient:
    address = "ws://127.0.0.1:4000"

    @classmethod
    def post_to_ws(cls, body):
        ws = websocket.WebSocket()
        ws.connect(cls.address)
        if not isinstance(body, str):
            if isinstance(body, BaseModel):
                body = json.dumps(body.dict())
            else:
                body = json.loads(json.dumps(json.dumps(body, default=lambda x: x.__dict__)))
        ws.send(body)
        response = ws.recv()
        ws.close()
        return response

