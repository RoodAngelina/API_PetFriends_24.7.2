import json
import requests


class PetFriends:
    """API библиотека к веб-приложению Pet Friends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат
        в формате JSON с уникальным ключом пользователя, найденным по указанным email и паролю."""

        headers = {'email': email, 'password': passwd}
        r = requests.get(self.base_url + 'api/key', headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение '' - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев."""

        headers = {'auth_key': auth_key['key']}
        params = {'filter': filter}
        r = requests.get(self.base_url + 'api/pets', params=params, headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
        запроса и результат в формате JSON с данными добавленного питомца."""

        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        r = requests.post(self.base_url + 'api/pets', data=data, headers=headers, files=file)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному id и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом 200."""

        headers = {'auth_key': auth_key['key']}
        r = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному id и
        возвращает статус запроса и результат в формате JSON с обновлёнными данными питомца."""

        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        r = requests.put(self.base_url + 'api/pets/' + pet_id, data=data, headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце без фото и возвращает статус
        запроса и результат в формате JSON с данными добавленного питомца без фото."""

        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        r = requests.post(self.base_url + 'api/create_pet_simple', data=data, headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result

    def add_photo_of_a_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер фото питомца по указанному ID и
        возвращает статус запроса и результат в формате JSON с данными питомца, в том числе добавленным фото."""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        r = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, files=file, headers=headers)
        status = r.status_code
        try:
            result = r.json()
        except json.decoder.JSONDecodeError:
            result = r.text
        return status, result
