import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/messenger.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # RESTful парсеры
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB для файлов
    UPLOAD_FOLDER = 'static/uploads'

    # Разработка
    DEBUG = True