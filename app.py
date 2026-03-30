from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import Chat, User
from api import api
from werkzeug.utils import secure_filename
import os

# Глобальные объекты
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация
    db.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)

    # Создание папки для файлов
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Flask-Login loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()  # Создаёт таблицы

        # Тестовые данные (если нужно будет - добавлю, елки палки)
        if not User.query.first():
            # Создать тестового юзера
            pass

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='127.0.0.1', port=5000)