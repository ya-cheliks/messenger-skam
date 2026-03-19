### Flask Messenger MVP
Простой текстовый мессенджер для школьного проекта по Flask. Пользователи регистрируются, логинятся и общаются чатах.

## MVP Функционал:

 - Регистрация/авторизация пользователей

 - Отправка и просмотр текстовых сообщений

 - Responsive дизайн с Bootstrap

## Технологии
```text
Backend: Flask + Blueprints + SQLAlchemy (SQLite)
Auth: Flask-Login + WTForms
Frontend: Bootstrap 5 + HTML/CSS/JS
Хранение: SQLite (модели User, Message)
Развертывание: позже
```
## Структура проекта
```text
messenger/
├── app.py           # Главный файл
├── config.py        # Настройки
├── models.py        # ORM модели
├── auth/           # Blueprints: авторизация
├── chat/           # Blueprints: чат
├── templates/      # HTML с Bootstrap
└── static/         # CSS/JS
```
## Быстрый старт
```bash
pip install -r requirements.txt
flask run
```
