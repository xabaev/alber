import unittest
import uuid
from random import randrange

import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse, SelectUser
from api.models.tester_response import TesterResponse
from tests.base_test import BaseTest, ordering


class TestSelectUser(BaseTest, unittest.TestCase):
    @pytest.mark.xfail(reason="Always comes back failure")
    def test_select_existing_user_by_phone(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert result == expected_result

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=add_user.phone)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                      phone=add_user.phone, age=add_user.age)])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    @pytest.mark.xfail(reason="In my opinion, the absence of a user is not a failure")
    def test_get_nonexistent_user_by_phone(self):
        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=-1)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success")
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure")
    def test_select_existing_user_by_name(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name=str(uuid.uuid4()), surname="surname",
                           phone=str(uuid.uuid4()), age=100)
        expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert result == expected_result

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", name=add_user.name)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                      phone=add_user.phone, age=add_user.age)])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure")
    def test_select_existing_user_by_surname(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname=str(uuid.uuid4()),
                           phone=str(uuid.uuid4()), age=100)
        expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert result == expected_result

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", surname=add_user.surname)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                      phone=add_user.phone, age=add_user.age)])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure + bug - only one result is returned")
    def test_select_existing_several_users_by_surname(self):
        surname = str(uuid.uuid4())
        add_user1 = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname=surname,
                            phone=str(uuid.uuid4()), age=100)
        expected_result1 = TesterResponse(id=add_user1.id, method=add_user1.method, status="success")
        result1 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user1))

        assert result1 == expected_result1

        add_user2 = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname=surname,
                            phone=str(uuid.uuid4()), age=0)
        expected_result2 = TesterResponse(id=add_user2.id, method=add_user2.method, status="success")
        result2 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user2))

        assert result2 == expected_result2

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", surname=surname)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[SelectUser(name=add_user1.name, surname=add_user1.surname,
                                                                      phone=add_user1.phone, age=add_user1.age),
                                                           SelectUser(name=add_user2.name, surname=add_user2.surname,
                                                                      phone=add_user2.phone, age=add_user2.age)
                                                           ])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert ordering(select_result.dict()) == ordering(expected_select_result.dict())

    @pytest.mark.xfail(reason="Always comes back failure")
    def test_select_existing_several_users_by_name(self):
        name = str(uuid.uuid4())
        add_user1 = AddUser(id=str(uuid.uuid4()), method="add", name=name, surname="surname",
                            phone=str(uuid.uuid4()), age=100)
        expected_result1 = TesterResponse(id=add_user1.id, method=add_user1.method, status="success")
        result1 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user1))

        assert result1 == expected_result1

        add_user2 = AddUser(id=str(uuid.uuid4()), method="add", name=name, surname="surname",
                            phone=str(uuid.uuid4()), age=0)
        expected_result2 = TesterResponse(id=add_user2.id, method=add_user2.method, status="success")
        result2 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user2))

        assert result2 == expected_result2

        add_user3 = AddUser(id=str(uuid.uuid4()), method="add", name=name, surname="surname",
                            phone=str(uuid.uuid4()), age=0)
        expected_result3 = TesterResponse(id=add_user3.id, method=add_user3.method, status="success")
        result3 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user3))

        assert result3 == expected_result3

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", name=name)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[SelectUser(name=add_user1.name, surname=add_user1.surname,
                                                                      phone=add_user1.phone, age=add_user1.age),
                                                           SelectUser(name=add_user2.name, surname=add_user2.surname,
                                                                      phone=add_user2.phone, age=add_user2.age),
                                                           SelectUser(name=add_user3.name, surname=add_user3.surname,
                                                                      phone=add_user3.phone, age=add_user3.age)
                                                           ])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert ordering(select_result.dict()) == ordering(expected_select_result.dict())
