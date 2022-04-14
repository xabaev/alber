import uuid
from random import randrange

import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.delete_user import DeleteUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse, SelectUser
from api.models.tester_response import TesterResponse
from api.models.update_user import UpdateUser
from tests.base_test import BaseTest


class TestUpdateUser(BaseTest):

    @pytest.mark.xfail(reason="Select always comes back failure + bug in update - age is not updated")
    def test_should_see_success_after_update_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert add_result == expected_result_add

        update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                 phone=add_user.phone, age=30)
        expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
        result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

        assert result_update == expected_result_update

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[
                                                        SelectUser(name=update_user.name, surname=update_user.surname,
                                                                   phone=update_user.phone, age=update_user.age)])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Select always comes back failure + bug in update - age is not updated")
    def test_should_see_success_after_update_user_twice(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert add_result == expected_result_add

        update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                 phone=add_user.phone, age=30)
        expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
        result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

        assert result_update == expected_result_update

        update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name2", surname="surname2",
                                 phone=add_user.phone, age=60)
        expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
        result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

        assert result_update == expected_result_update

        select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
        expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                    users=[
                                                        SelectUser(name=update_user.name, surname=update_user.surname,
                                                                   phone=update_user.phone, age=update_user.age)])
        select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

        assert select_result == expected_select_result

    def test_should_see_failure_after_update_nonexist_user(self):
        update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                 phone=str(randrange(0, 50000)), age=30)
        expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="failure")
        result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

        assert result_update == expected_result_update

    def test_should_see_failure_after_update_deleted_user(self):
        add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
        expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
        add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

        assert add_result == expected_result_add

        delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
        expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
        delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

        assert delete_result == expected_result_delete
        update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                 phone=add_user.phone, age=30)
        expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="failure")
        result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

        assert result_update == expected_result_update
