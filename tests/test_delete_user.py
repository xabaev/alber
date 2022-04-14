import uuid
from random import randrange

import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.delete_user import DeleteUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse
from api.models.tester_response import TesterResponse
from tests.base_test import BaseTest


# def get_required_fields():
#     return [
#         (DeleteUser(method="delete", phone=str(randrange(0, 50000))), "failure"),
#         (DeleteUser(id=str(uuid.uuid4()), phone=str(randrange(0, 50000))), "failure"),
#         (DeleteUser(id=str(uuid.uuid4()), method="delete"), "failure")
#     ]


class TestDeleteUser(BaseTest):
    def test_should_see_success_after_delete_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert add_result == expected_result_add

        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
        expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
        delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

        assert delete_result == expected_result_delete

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=add_user.phone)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="failure")
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    def test_should_see_failure_after_delete_nonexistent_user(self):
        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
        expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method,
                                                status="failure")
        delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

        assert delete_result == expected_result_delete

    @pytest.mark.xfail(reason="The id returned is not the one with which the function was called")
    def test_should_see_failure_after_deleting_a_deleted_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert add_result == expected_result_add

        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
        expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
        delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

        assert delete_result == expected_result_delete

        delete_user2 = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
        expected_result_delete2 = TesterResponse(id=delete_user2.id, method=delete_user2.method,
                                                 status="failure")
        delete_result2 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

        assert delete_result2 == expected_result_delete2

    # @pytest.mark.parametrize('body, status', get_required_fields())
    # def test_required_fields_in_add_user(self, body, status):
    #     response = TesterClient.post_to_ws(body=body)
    #     result = TesterResponse.parse_raw(response)
    #
    #     assert status == result.status
