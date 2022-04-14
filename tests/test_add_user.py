import uuid
from random import randrange

import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.tester_response import TesterResponse
from tests.base_test import BaseTest


# def get_required_fields():
#     return [(AddUser(method="add", name="name", surname="surname",
#                      phone=str(randrange(0, 50000)), age=100), "failure"),
#             (AddUser(id=str(uuid.uuid4()), name="name", surname="surname",
#                      phone=str(randrange(0, 50000)), age=100), "failure"),
#             (AddUser(id=str(uuid.uuid4()), method="add", surname="surname",
#                      phone=str(randrange(0, 50000)), age=100), "failure"),
#             (AddUser(id=str(uuid.uuid4()), method="add", name="name",
#                      phone=str(randrange(0, 50000)), age=100), "failure"),
#             (AddUser(id=str(uuid.uuid4()), method="add", name="name",
#                      surname="surname", age=100), "failure"),
#             (AddUser(id=str(uuid.uuid4()), method="add", name="name",
#                      surname="surname",
#                      phone=str(randrange(0, 50000))), "failure")]


class TestAddUser(BaseTest):
    def test_should_see_success_after_add_user(self):
        user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                       phone=str(randrange(0, 50000)), age=100)

        expected_result = TesterResponse(id=user.id, method=user.method, status="success")
        result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

        assert result == expected_result

    @pytest.mark.xfail(reason="The id returned is not the one with which the function was called")
    def test_should_see_failed_after_add_user_by_existing_user(self):
        user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                       phone=str(randrange(0, 50000)), age=100)
        expected_result = TesterResponse(id=user.id, method=user.method, status="success")
        result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

        assert result == expected_result

        another_user = AddUser(id=str(uuid.uuid4()), method="add", name="name1", surname="surname1",
                               phone=user.phone, age=101)
        another_expected_result = TesterResponse(id=another_user.id, method=another_user.method, status="failure")
        another_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

        assert another_result == another_expected_result

#    @pytest.mark.parametrize('user, status', get_required_fields())
#    def test_required_fields_in_add_user(self, user, status):
#        response = TesterClient.post_to_ws(body=user)
#        result = TesterResponse.parse_raw(response)
#
#        assert status == result.status
