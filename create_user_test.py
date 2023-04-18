import data
import sender_stand_request


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name

    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    user_content = user_response.json()

    assert user_response.status_code == 400
    assert user_content['code'] == 400
    assert user_content['message'] == 'Имя пользователя введено некорректно. Имя может содержать только русские или ' \
                                      'латинские буквы, длина должна быть не менее 2 и не более 15 символов'


def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == 'Не все необходимые параметры были переданы'


# Тест 1. Допустимое количество символов (2)
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert('Aa')


# Тест 2. Допустимое количество символов (15)
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert('Aaааааааааааааа')


# Тест 3. Количество символов меньше допустимого (1)
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol('А')


# Тест 4. Количество символов больше допустимого (16)
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol('Аааааааааааааааа')


# Тест 5. Разрешены английские буквы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert('QWErty')


# Тест 6. Разрешены русские символы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert('Мария')


# Тест 7. Запрещены пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol('Человек и Ко')


# Тест 8. Запрещены спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol('№%@')


# Тест 9. Запрещены цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol('123')


# Тест 10. Параметр не передан в запросе
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


# Тест 11. Передано пустое значение параметра
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


# Тест 12. Передан другой тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400