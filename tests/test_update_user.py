import uuid
from random import randrange

import allure
import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.delete_user import DeleteUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse, SelectUser
from api.models.tester_response import TesterResponse
from api.models.update_user import UpdateUser


class TestUpdateUser:

    @pytest.mark.xfail(reason="Select always comes back failure + bug in update - age is not updated")
    @allure.feature('Update user')
    @allure.story('Update user')
    @allure.description('Get: Preparing data via addUser. '
                        'Then: Update all fields in user. '
                        'After: Check fields in user via selectUser.')
    def test_should_see_success_after_update_user(self):
        with allure.step(f"Prepare user in db"):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert add_result == expected_result_add

        with allure.step(f"Updating all user fields"):
            update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                     phone=add_user.phone, age=30)
            expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
            result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

            assert result_update == expected_result_update

        with allure.step(f'Check that the user is updated (via select)'):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[
                                                            SelectUser(name=update_user.name,
                                                                       surname=update_user.surname,
                                                                       phone=update_user.phone, age=update_user.age)])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Select always comes back failure + bug in update - age is not updated")
    @allure.feature('Update user')
    @allure.story('Update user twice')
    @allure.description('Get: Preparing data via addUser. '
                        'Then: Update all fields in user twice. '
                        'After: Check fields in user via selectUser.')
    def test_should_see_success_after_update_user_twice(self):
        with allure.step(f"Prepare user in db"):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert add_result == expected_result_add

        with allure.step(f"Updating all user fields"):
            update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                     phone=add_user.phone, age=30)
            expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
            result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

            assert result_update == expected_result_update

        with allure.step(f"Updating all user fields a second time"):
            update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name2", surname="surname2",
                                     phone=add_user.phone, age=60)
            expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="success")
            result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

            assert result_update == expected_result_update

        with allure.step(f'Check that the user is updated (via select)'):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[
                                                            SelectUser(name=update_user.name,
                                                                       surname=update_user.surname,
                                                                       phone=update_user.phone, age=update_user.age)])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @allure.feature('Update user')
    @allure.story('Update nonexistent user')
    @allure.description('Get: Nothing. '
                        'Then: Update all fields in nonexistent user. '
                        'After: Check existent user via selectUser.')
    def test_should_see_failure_after_update_nonexistent_user(self):
        with allure.step(f"Updating all fields of a nonexistent user"):
            update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                     phone=str(randrange(0, 50000)), age=30)
            expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="failure")
            result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

            assert result_update == expected_result_update

        with allure.step(f'Check that the user is non exist (via select)'):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="failure")
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @allure.feature('Update user')
    @allure.story('Update deleted user')
    @allure.description('Get: Preparing data via addUser and deleteUser. '
                        'Then: Update all fields in deleted user. '
                        'After: Check deleted user via selectUser.')
    def test_should_see_failure_after_update_deleted_user(self):
        with allure.step(f"Preparing a deleted user in the database"):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert add_result == expected_result_add

            delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
            expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
            delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

            assert delete_result == expected_result_delete

        with allure.step(f"Updating all fields of a deleted user"):
            update_user = UpdateUser(id=str(uuid.uuid4()), method="update", name="name1", surname="surname1",
                                     phone=add_user.phone, age=30)
            expected_result_update = TesterResponse(id=update_user.id, method=update_user.method, status="failure")
            result_update = TesterResponse.parse_raw(TesterClient.post_to_ws(body=update_user))

            assert result_update == expected_result_update

        with allure.step(f'Check that the user is non exist (via select)'):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=update_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="failure")
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result
