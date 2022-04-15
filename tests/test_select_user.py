import uuid
from random import randrange

import allure
import pytest

from api.clients.tester_client import TesterClient
from api.commons.sorting import ordering
from api.models.add_user import AddUser
from api.models.select.select_user_request import SelectUserRequest
from api.models.select.select_user_response import SelectUserResponse, SelectUser
from api.models.tester_response import TesterResponse


class TestSelectUser:
    @pytest.mark.xfail(reason="Always comes back failure")
    @allure.feature('Select user')
    @allure.story('Select existing user')
    @allure.description('Get: Preparing data via addUser. \n'
                        'Then: Select the user with the phone. \n'
                        'After: Check all fields for the selected user.')
    def test_select_existing_user_by_phone(self):
        with allure.step(f'Prepare user in db'):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname="surname",
                               phone=str(randrange(0, 50000)), age=100)
            expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert result == expected_result

        with allure.step(f"Retrieve a user via the phone and check that the user exists and that his model is correct"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=add_user.phone)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                          phone=add_user.phone, age=add_user.age)])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @pytest.mark.xfail(reason="In my opinion, the absence of a user is not a failure")
    @allure.feature('Select user')
    @allure.story('Select nonexistent user by phone')
    @allure.description('Get: Nothing. \n'
                        'Then: Select the user with the unknown phone. \n'
                        'After: Check the status and absence of users.')
    def test_get_nonexistent_user_by_phone(self):
        with allure.step(f"Check that the non-existent user does not exist"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", phone=-1)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success")
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure")
    @allure.feature('Select user')
    @allure.story('Select existing user by name')
    @allure.description('Get: Preparing data via addUser. \n'
                        'Then: Select the user with the name. \n'
                        'After: Check all fields for the selected user.')
    def test_select_existing_user_by_name(self):
        with allure.step(f"Prepare user in db"):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name=str(uuid.uuid4()), surname="surname",
                               phone=str(uuid.uuid4()), age=100)
            expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert result == expected_result

        with allure.step(f"Retrieve a user via the name and check that the user exists and that his model is correct"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", name=add_user.name)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                          phone=add_user.phone, age=add_user.age)])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure")
    @allure.feature('Select user')
    @allure.story('Select existing user by surname')
    @allure.description('Get: Preparing data via addUser. \n'
                        'Then: Select the user with the surname. \n'
                        'After: Check all fields for the selected user.')
    def test_select_existing_user_by_surname(self):
        with allure.step(f"Prepare user in db"):
            add_user = AddUser(id=str(uuid.uuid4()), method="add", name="name", surname=str(uuid.uuid4()),
                               phone=str(uuid.uuid4()), age=100)
            expected_result = TesterResponse(id=add_user.id, method=add_user.method, status="success")
            result = TesterResponse.parse_raw(TesterClient.post_to_ws(body=add_user))

            assert result == expected_result

        with allure.step(
                f"Retrieve a user via the surname and check that the user exists and that his model is correct"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", surname=add_user.surname)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[SelectUser(name=add_user.name, surname=add_user.surname,
                                                                          phone=add_user.phone, age=add_user.age)])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert select_result == expected_select_result

    @pytest.mark.xfail(reason="Always comes back failure + bug - only one result is returned")
    @allure.feature('Select user')
    @allure.story('Select several users by surname')
    @allure.description('Get: Preparing data via addUser. \n'
                        'Then: Select the users with the surname. \n'
                        'After: Check all fields for the selected users.')
    def test_select_existing_several_users_by_surname(self):
        with allure.step(f"Prepare two users in db"):
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

        with allure.step(f"Get users by surname and check that they exist and that his model is correct"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", surname=surname)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[
                                                            SelectUser(name=add_user1.name, surname=add_user1.surname,
                                                                       phone=add_user1.phone, age=add_user1.age),
                                                            SelectUser(name=add_user2.name, surname=add_user2.surname,
                                                                       phone=add_user2.phone, age=add_user2.age)
                                                        ])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert ordering(select_result.dict()) == ordering(expected_select_result.dict())

    @pytest.mark.xfail(reason="Always comes back failure")
    @allure.feature('Select user')
    @allure.story('Select several users by name')
    @allure.description('Get: Preparing data via addUser. \n'
                        'Then: Select the users with the name. \n'
                        'After: Check all fields for the selected users.')
    def test_select_existing_several_users_by_name(self):
        with allure.step(f"Prepare three users in db"):
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

        with allure.step(f"Get users by surname and check that they exist and that his model is correct"):
            select_user = SelectUserRequest(id=str(uuid.uuid4()), method="select", name=name)
            expected_select_result = SelectUserResponse(id=select_user.id, method="select", status="success",
                                                        users=[
                                                            SelectUser(name=add_user1.name, surname=add_user1.surname,
                                                                       phone=add_user1.phone, age=add_user1.age),
                                                            SelectUser(name=add_user2.name, surname=add_user2.surname,
                                                                       phone=add_user2.phone, age=add_user2.age),
                                                            SelectUser(name=add_user3.name, surname=add_user3.surname,
                                                                       phone=add_user3.phone, age=add_user3.age)
                                                        ])
            select_result = SelectUserResponse.parse_raw(TesterClient.post_to_ws(body=select_user))

            assert ordering(select_result.dict()) == ordering(expected_select_result.dict())
