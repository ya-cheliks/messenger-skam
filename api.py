from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)

chat_parser = reqparse.RequestParser()
chat_parser.add_argument('name', type=str, required=True)
chat_parser.add_argument('users_id', type=str, required=True)
chat_parser.add_argument('is_private', type=bool, default=False)