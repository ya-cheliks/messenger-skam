import base64
import requests


def get_map_data_uri(ll):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    map_request = f"{server_address}ll={ll}&apikey={api_key}&spn=0.05,0.05&pt={ll}"
    response = requests.get(map_request)
    response.raise_for_status()
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


def ll(test_mass):
    try:
        loc = test_mass[4:]
        ll_uri_map = materic(loc)
        print(ll_uri_map[:100])
    except Exception:
        ll_uri_map = None
    finally:
        return ll_uri_map


if __name__ == '__main__':
    name_geo = 'Москва'
    print(get_map_data_uri(name_geo).content)
