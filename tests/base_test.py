import unittest

from api.clients.tester_client import TesterClient


def setup_method(method):
    print("setup_method")
    # self.ws = self.testerClient.connect_to_ws()


def teardown_method(method):
    print("teardown_method")
    # self.testerClient.disconnect_from_ws(self.ws)


def ordering(obj):
    if isinstance(obj, dict):
        return sorted((k, ordering(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordering(x) for x in obj)
    else:
        return obj


class BaseTest(unittest.TestCase):
    testerClient = TesterClient()
