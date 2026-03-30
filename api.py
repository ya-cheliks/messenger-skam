from flask_restful import Api, reqparse
from app import app
from resources import UserResource, ChatResource

api = Api(app)

# Парсеры
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)

chat_parser = reqparse.RequestParser()
chat_parser.add_argument('name', type=str, required=True)
chat_parser.add_argument('users_id', type=str, required=True)
chat_parser.add_argument('is_private', type=bool)

# Регистрация маршрутов
api.add_resource(UserResource, '/api/users/<int:user_id>', '/api/users')
api.add_resource(ChatResource, '/api/chats/<int:chat_id>', '/api/chats')