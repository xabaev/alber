import uuid
from random import randrange
from typing import List

from api.models.add_user import AddUser
from api.clients.tester_client import TesterClient
from api.models.select.select_user import SelectUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse
from api.models.tester_response import TesterResponse
from tests.base_test import BaseTest


class TestSelectUser(BaseTest):
    def test_select_user_by_phone(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result = TesterResponse(id=add_user["id"], method=add_user["method"], status="success")
        result = TesterResponse.from_json(TesterClient.post_to_ws(body=add_user))

        assert expected_result == result

        my_list: List[SelectUser] = [SelectUser(name=add_user["name"], surname=add_user["surname"],
                                                phone=add_user["phone"], age=add_user["age"])]
        my_list2 = list[SelectUser(name=add_user["name"], surname=add_user["surname"],
                                   phone=add_user["phone"], age=add_user["age"])]
        print("WHAT IS THAT? " + str(type(my_list)))
        print("WHAT IS THAT2? " + str(type(my_list2)))

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=add_user["phone"])
        expected_select_result = SelectUserResponse(id=select_user["id"], method="select", status="success",
                                                    users=my_list)
        select_result = SelectUserResponse.from_json(TesterClient.post_to_ws(body=select_user))

        assert expected_select_result == select_result
