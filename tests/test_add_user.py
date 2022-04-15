import uuid
from random import randrange

import allure
import pytest

from api.clients.tester_client import TesterClient
from api.models.add_user import AddUser
from api.models.tester_response import TesterResponse


class TestAddUser:

    @allure.feature('Add user')
    @allure.story('Success add user')
    @allure.description('Get: Nothing '
                        'Then: Add the user. '
                        'After: Checking the "success" status after the addition.')
    def test_should_see_success_after_add_user(self):
        with allure.step(f'Send user to service'):
            user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)

            expected_result = TesterResponse(id=user.id, method=user.method, status="success")
            result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

            assert result == expected_result

    @pytest.mark.xfail(reason="The id returned is not the one with which the function was called")
    @allure.feature('Add user')
    @allure.story('Add existing user')
    @allure.description('Get: Nothing '
                        'Then: Add the user twice. '
                        'After: Checking the "failure" status after the second addition.')
    def test_should_see_failed_after_add_user_by_existing_user(self):
        with allure.step(f'Send user to service'):
            user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                           phone=str(randrange(0, 50000)), age=100)
            expected_result = TesterResponse(id=user.id, method=user.method, status="success")
            result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

            assert result == expected_result

        with allure.step(f'Send another user to service'):
            another_user = AddUser(id=str(uuid.uuid4()), method="add", name="name1", surname="surname1",
                                   phone=user.phone, age=101)
            another_expected_result = TesterResponse(id=another_user.id, method=another_user.method, status="failure")
            another_result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=user))

            assert another_result == another_expected_result
