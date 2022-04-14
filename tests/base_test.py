from api.clients.tester_client import TesterClient


def setup_method(method):
    print("setup_method")
    # self.ws = self.testerClient.connect_to_ws()


def teardown_method(method):
    print("teardown_method")
    # self.testerClient.disconnect_from_ws(self.ws)


class BaseTest:
    testerClient = TesterClient()
