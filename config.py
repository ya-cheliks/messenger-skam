import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skam-secret-key-123'  # для школы сойдёт
    SQLALCHEMY_DATABASE_URI = 'sqlite:///skam.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False