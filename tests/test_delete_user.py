import uuid
from random import randrange

import allure
import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.delete_user import DeleteUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse
from api.models.tester_response import TesterResponse


class TestDeleteUser:
    @allure.feature('Delete user')
    @allure.story('Delete existing user')
    @allure.description('Get: Preparing data via addUser. '
                        'Then: Delete the user. '
                        'After: Check deleted user via selectUser.')
    def test_should_see_success_after_delete_user(self):
        with allure.step(f'Prepare user in db'):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert add_result == expected_result_add

        with allure.step(f'Delete user'):
            delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
            expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
            delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

            assert delete_result == expected_result_delete

        with allure.step(f'Check that the user is deleted (via select)'):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=add_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="failure")
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @allure.feature('Delete user')
    @allure.story('Delete nonexistent user')
    @allure.description('Get: Nothing. '
                        'Then: Delete the user. '
                        'After: Checking the "failure" status after the deletion.')
    def test_should_see_failure_after_delete_nonexistent_user(self):
        with allure.step(f'Delete nonexistent user'):
            delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
            expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method,
                                                    status="failure")
            delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

            assert delete_result == expected_result_delete

    @pytest.mark.xfail(reason="The id returned is not the one with which the function was called")
    @allure.feature('Delete user')
    @allure.story('Delete a deleted user')
    @allure.description('Get: Preparing data via addUser '
                        'Then: Delete the user twice. '
                        'After: Checking the "failure" status after the second deletion')
    def test_should_see_failure_after_deleting_a_deleted_user(self):
        with allure.step(f'Prepare user in db'):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result_add = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            add_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert add_result == expected_result_add

        with allure.step(f'Delete user'):
            delete_user = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=add_user.phone)
            expected_result_delete = TesterResponse(id=delete_user.id, method=delete_user.method, status="success")
            delete_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

            assert delete_result == expected_result_delete

        with allure.step(f'A second time delete this user'):
            delete_user2 = DeleteUser(id=str(uuid.uuid4()), method="delete", phone=str(randrange(0, 50000)))
            expected_result_delete2 = TesterResponse(id=delete_user2.id, method=delete_user2.method,
                                                     status="failure")
            delete_result2 = TesterResponse.parse_raw(TesterClient.post_to_ws(body=delete_user))

            assert delete_result2 == expected_result_delete2
