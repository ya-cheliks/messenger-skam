import requests


def get_map_data_uri(name_geo):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    ll_spn = f'll={materic(name_geo)}'
    # Готовим запрос.

    map_request = f"{server_address}{ll_spn}&apikey={api_key}&spn=0.15,0.15"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
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
