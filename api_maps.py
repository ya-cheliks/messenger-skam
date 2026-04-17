import base64

import requests


def get_map_data_uri(name_geo):
    # 1. Получаем координаты
    ll = materic(name_geo)

    # 2. Формируем запрос к статическим картам
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    map_request = f"{server_address}ll={ll}&apikey={api_key}&spn=0.15,0.15"

    response = requests.get(map_request)
    response.raise_for_status()  # Проверка на ошибки HTTP (404, 403 и т.д.)

    # 3. Определяем MIME-тип (обычно image/png или image/jpeg)
    content_type = response.headers.get('Content-Type', 'image/png')

    # 4. Кодируем бинарные данные в base64
    # b64_encoded = base64.b64encode(response.content) #.decode('utf-8')

    # 5. Формируем Data URI в том же формате, что у вас
    # data_uri = f"data:{content_type};base64,{b64_encoded}"
    return response.content


def materic(name):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocodes = [name]
    for geocode in geocodes:
        # Готовим запрос.
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

        # Выполняем запрос.
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return ','.join(toponym_coodrinates.split(" "))


if __name__ == '__main__':
    name_geo = 'Москва'
    print(getImage(name_geo).content)
