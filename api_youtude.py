import requests


API_KEY = "AIzaSyC_7eXlBOrQfwMB17qmnT1xpUEy3y9SXjw"


def youtube_https(title):
    try:
        title = title[4:]
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "id",
            "q": title,
            "type": "video",
            "maxResults": 1,
            "key": API_KEY
        }

        response = requests.get(url, params=params).json()
        video_id = response["items"][0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        video_url = None
    finally:
        return video_url


def channel_by_name(channel_name):
    """
    Ищет канал YouTube по названию.
    Возвращает ссылку на канал или None, если не найдено.
    """
    channel_name = channel_name[4:]
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",  # Получаем базовую информацию (название, описание, картинка)
        "q": channel_name,  # Поисковый запрос
        "type": "channel",  # Ищем ТОЛЬКО каналы
        "maxResults": 1,  # Берем самый релевантный результат
        "key": API_KEY  # Ваш API ключ
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP (403, 404 и т.д.)
        data = response.json()

        if not data.get("items"):
            return None

        # Извлекаем ID канала
        channel_id = data["items"][0]["id"]["channelId"]
        channel_title = data["items"][0]["snippet"]["title"]

        # Формируем ссылку
        channel_url = f"https://www.youtube.com/channel/{channel_id}"

        return {
            "title": channel_title,
            "url": channel_url,
            "id": channel_id
        }

    except requests.exceptions.HTTPError as e:
        return None