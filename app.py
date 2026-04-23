from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from data.model_chat import Chat
from data.model_user import User
from werkzeug.utils import secure_filename
import os
from data import db_session
from auth import auth
from chat import chat
from flask_restful import Api
from resources import UserResource, ChatResource, MessageResource

# Глобальные объекты
db = SQLAlchemy()
db_session.global_init('db/skam.db')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app)
    api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(ChatResource, '/api/chats', '/api/chats/<int:chat_id>')
    api.add_resource(MessageResource, '/api/chats/messages/<int:chat_id>', '/api/messages/<int:message_id>')

    # Инициализация
    db.init_app(app)
    login_manager.init_app(app)

    # Создание папки для файлов
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Flask-Login loader
    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        try:
            return session.get(User, user_id)
        finally:
            session.close()

    app.register_blueprint(auth)

    app.register_blueprint(chat)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='127.0.0.1', port=5000)