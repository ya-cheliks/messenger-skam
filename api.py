from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)

chat_parser = reqparse.RequestParser()
chat_parser.add_argument('name', type=str, required=True)
chat_parser.add_argument('users_id', type=str, required=True)
chat_parser.add_argument('is_private', type=bool, default=False)

message_parser = reqparse.RequestParser()
message_parser.add_argument('content', type=str, required=True)
# message_parser.add_argument('chat_id', type=int, required=True)
message_parser.add_argument('sender_id', type=int, required=True)
message_parser.add_argument('picture', type=str, required=False)
message_parser.add_argument('coordinates', type=str, required=False)