import uuid
from random import randrange

import pytest

from api.models.add_user import AddUser
from api.clients.tester_client import TesterClient
from api.models.delete_user import DeleteUser
from api.models.tester_response import TesterResponse
from tests.base_test import BaseTest


def get_required_fields():
    return [
        (DeleteUser(method="delete", phone=str(randrange(0, 50000))), "failure"),
        (DeleteUser(id=str(uuid.uuid4()), phone=str(randrange(0, 50000))), "failure"),
        (DeleteUser(id=str(uuid.uuid4()), method="delete"), "failure")
    ]


class TestAddUser(BaseTest):
    def test_should_see_success_after_delete_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user["id"], method=add_user["method"], status="success")
        add_result = TesterResponse.from_json(TesterClient.post_to_ws(body=add_user))

        assert expected_result_add == add_result

        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user["phone"])
        expected_result_delete = TesterResponse(id=delete_user["id"], method=delete_user["method"], status="success")
        delete_result = TesterResponse.from_json(TesterClient.post_to_ws(body=delete_user))

        assert expected_result_delete == delete_result

    def test_should_see_failure_after_delete_nonexistent_user(self):
        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
        expected_result_delete = TesterResponse(id=delete_user["id"], method=delete_user["method"],
                                                status="failure")
        delete_result = TesterResponse.from_json(TesterClient.post_to_ws(body=delete_user))

        assert expected_result_delete == delete_result

    @pytest.mark.xfail(reason="The id returned is not the one with which the function was called")
    def test_should_see_failure_after_deleting_a_deleted_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user["id"], method=add_user["method"], status="success")
        add_result = TesterResponse.from_json(TesterClient.post_to_ws(body=add_user))

        assert expected_result_add == add_result

        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user["phone"])
        expected_result_delete = TesterResponse(id=delete_user["id"], method=delete_user["method"], status="success")
        delete_result = TesterResponse.from_json(TesterClient.post_to_ws(body=delete_user))

        assert expected_result_delete == delete_result

        delete_user2 = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
        expected_result_delete2 = TesterResponse(id=delete_user2["id"], method=delete_user2["method"],
                                                 status="failure")
        delete_result2 = TesterResponse.from_json(TesterClient.post_to_ws(body=delete_user))

        assert expected_result_delete2 == delete_result2

    @pytest.mark.parametrize('body, status', get_required_fields())
    def test_required_fields_in_add_user(self, body, status):
        response = TesterClient.post_to_ws(body=body)
        result = TesterResponse.from_json(response)

        assert result["status"] == status
