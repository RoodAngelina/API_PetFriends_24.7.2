from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_invalid_user(email='rood.angelina@gmail.com', password='lalala'):
    """Проверяем, что запрос api ключа с незарегестированного ранее email возвращает код статуса 403
    и в ответе не содержится слово key."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_invalid_password(email=valid_email, password='lalala'):
    """Проверяем, что запрос api ключа при неверно введённом пароле возвращает код статуса 403
    и в ответе не содержится слово key."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'key' not in result


def test_get_api_key_without_user(email='', password=''):
    """Проверяем, что без email и password запрос api ключа возвращает код статуса 403
    и в ответе не содержится слово key."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
    """Используя невалидный ключ, запрашиваем список всех питомцев и проверяем, что код статуса 403
    и ответ не содержит список питомцев."""

    auth_key = {'key': '123'}

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'pets' not in result


def test_get_my_pets_with_invalid_key(filter='my_pets'):
    """Используя невалидный ключ, запрашиваем список своих питомцев и проверяем, что код статуса 403
    и ответ не содержит список питомцев."""

    auth_key = {'key': '123'}

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'pets' not in result


def test_add_new_pet_with_photo_with_empty_data(name='', animal_type='', age='', pet_photo='images/hurma.jpg'):
    """Проверяем, что нельзя добавить питомца с пустыми данными имени, типа животного, возраста.
    Ожидаем: код статуса 400, в ответе нет id питомца с пустыми значениями, так как он не добавлен.
    На сегодняшний день тут есть баг - код статуса 200, в ответе содержится информация о добавленном
    питомце с пустыми данными имени, типа животного, возраста."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Отправляем запрос на добавление питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем ФР с ОР
    assert status == 400
    assert 'id' not in result


def test_add_new_pet_with_empty_data_without_photo(name='', animal_type='', age=''):
    """Проверяем, что нельзя добавить питомца с пустыми данными имени, типа животного, возраста,
    Ожидаем: код статуса 400, в ответе нет id питомца с пустыми значениями, так как он не добавлен.
    На сегодняшний день тут есть баг - код статуса 200, в ответе содержится информация о добавленном
    питомце с пустыми данными имени, типа животного, возраста."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Отправляем запрос на добавление питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ФР с ОР
    assert status == 400
    assert 'id' not in result


def test_add_new_pet_with_invalid_age(name='Кузя', animal_type='кот', age='!много'):
    """Проверяем, что нельзя добавить питомца с некорректными данными возраста.
    Ожидаем: код статуса 400, в ответе нет id питомца с некорректными данными возраста,
    так как он не добавлен. На сегодняшний день тут есть баг - код статуса 200,
    в ответе содержится информация о добавленном питомце с некорректными данными возраста."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    auth_key = pf.get_api_key(valid_email, valid_password)[1]

    # Отправляем запрос на добавление питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ФР с ОР
    assert status == 400
    assert 'id' not in result


def test_delete_not_my_pet():
    """Проверяем невозможность удаления питомца, добавленного другим пользователем.
    Ожидаем: код статуса 403, питомец по-прежнему в списке всех питомцев.
    На сегодняшний день тут есть баг - код статуса 200, питомец,
    добавленный другим пользователем, удаляется."""

    # Получаем ключ auth_key и запрашиваем список своих питомцев и список всех питомцев
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]
    all_pets = pf.get_list_of_pets(auth_key, '')[1]

    # Находим из списка всех питомцев питомца, добавленного другим пользователем,
    # и посылаем запрос на удаление этого питомца
    list_all_pets = all_pets['pets']
    list_id_my_pets = [my_pets['pets'][i]['id'] for i in range(len(my_pets['pets']))]
    for x in range(len(list_all_pets)):
        if list_all_pets[x]['id'] not in list_id_my_pets:
            pet_id_ = list_all_pets[x]['id']
            break
    status = pf.delete_pet(auth_key, pet_id_)[0]

    # Вновь запрашиваем список всех питомцев, и составляем список их id
    all_pets = pf.get_list_of_pets(auth_key, '')[1]
    list_id_all_pets = [all_pets['pets'][i]['id'] for i in range(len(all_pets['pets']))]

    # Сверяем ФР с ОР.
    assert status == 403
    assert pet_id_ in list_id_all_pets


def test_update_not_my_pet_info(name='Крендель', animal_type='собака', age='2'):
    """Проверяем невозможность обновления информации о питомце, добавленном другим пользователем.
    Ожидаем: код статуса 403, ответ не содержит информацию об обновлённом питомце, так как он не обновлён.
    На сегодняшний день тут есть баг - код статуса 200, в ответе содержится обновленная
    информация о питомце."""

    # Получаем ключ auth_key и запрашиваем список своих питомцев и список всех питомцев.
    auth_key = pf.get_api_key(valid_email, valid_password)[1]
    my_pets = pf.get_list_of_pets(auth_key, 'my_pets')[1]
    all_pets = pf.get_list_of_pets(auth_key, '')[1]

    # Находим из списка всех питомцев питомца, добавленного другим пользователем,
    # и посылаем запрос на обновление информации об этом питомце
    list_all_pets = all_pets['pets']
    list_id_my_pets = [my_pets['pets'][i]['id'] for i in range(len(my_pets['pets']))]
    for x in range(len(list_all_pets)):
        if list_all_pets[x]['id'] not in list_id_my_pets:
            pet_id_ = list_all_pets[x]['id']
            break
    status, result = pf.update_pet(auth_key, pet_id_, name, animal_type, age)

    # Сверяем ФР с ОР
    assert status == 403
    assert 'name' not in result and 'animal_type' not in result and 'age' not in result
