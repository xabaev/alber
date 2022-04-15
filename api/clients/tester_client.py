import asyncio
import configparser
import json

import websockets

from api.models.base_model import BaseModel

config = configparser.ConfigParser()
config.read("api/conf/cfg_test_environment.ini")
ADDRESS = config['WS']['address']


class TesterClient:

    @classmethod
    async def get_resp_from_ws(cls, body):
        if not isinstance(body, str):
            if isinstance(body, BaseModel):
                body = json.dumps(body.dict())
            else:
                body = json.loads(json.dumps(json.dumps(body, default=lambda x: x.__dict__)))

        async with websockets.connect(ADDRESS) as websocket:
            await websocket.send(body)
            response = await websocket.recv()
        return response

    @classmethod
    def post_to_ws(cls, body):
        return asyncio.get_event_loop().run_until_complete(cls.get_resp_from_ws(body))
