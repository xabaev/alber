# Tester.so
Решение тестового задания в Alber Blank

Реализация: Python 3.9. Pytest, Websocket, pydantic.

Инструкция по запуску тестов:
Из директории с тестами выполнить команду в терминале:
"docker build ./enviroment -t testerso"
"docker run -p 4000:4000 -t -i -d testerso"
"python3 -m pytest tests --alluredir \allure-results"

Инструкция по просмотру результатов:
Из директории с тестами выполнить команду в терминале "allure serve allure-results". Необходима установка allure (https://docs.qameta.io/allure/#_commandline).

Тесты не имеют подробного описания, а также отсутствует пачка аннотация для allure. Пропустил этот момент, так как не определенных правил, как отчет должен выглядеть.
Текущие падающие тесты замьючены xfail