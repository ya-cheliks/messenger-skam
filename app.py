from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # инициализация расширений
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # регистрация blueprint'ов
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from chat import chat as chat_bp
    app.register_blueprint(chat_bp)

    # создание БД при первом запуске
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)