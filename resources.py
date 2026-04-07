from flask_restful import reqparse, abort, Resource
from data import db_session
from flask import jsonify
from werkzeug.security import generate_password_hash
from data.model_user import User
from data.model_chat import Chat
from data.model_message import Message
from api import user_parser, chat_parser, message_parser
import base64


class UserResource(Resource):
    def get(self, user_id):
        self.abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)

        # Получаем ВСЕ чаты, где есть этот пользователь
        all_chats = session.query(Chat).all()
        user_chats = []

        for chat in all_chats:
            users_list = (chat.users_id or '').split()
            if str(user_id) in users_list:
                # Если чат приватный — показываем только участникам
                if chat.is_private and str(user_id) in users_list:
                    user_chats.append(chat)
                elif not chat.is_private:
                    user_chats.append(chat)

        return jsonify({
            'user': user.to_dict(only=('id', 'username', 'avatar')),
            'chats': [chat.to_dict(only=('id', 'name', 'is_private')) for chat in user_chats]
        })

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            username=args['username'],
            hashed_password=generate_password_hash(args['password'])
        )
        session.add(user)
        session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'status': 'registered'
        })

    def delete(self, user_id):
        self.abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_user_not_found(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if not user:
            abort(404, message=f"User {user_id} not found")


class ChatResource(Resource):
    def get(self):
        """возвращает список всех открытых чатов"""
        session = db_session.create_session()
        chats = session.query(Chat).filter_by(is_private=False).all()
        print(chats)
        if not chats:
            abort(404, message=f"Chats not found")
        return jsonify({'chats': [chat.to_dict(only=('id', 'name', 'is_private')) for chat in chats]})

    def post(self):
        args = chat_parser.parse_args()
        session = db_session.create_session()
        chat = Chat(
            name=args['name'],
            users_id=args['users_id'],
            is_private=args.get('is_private', False)
        )
        session.add(chat)
        session.commit()
        return jsonify({
            'id': chat.id,
            'name': chat.name,
            'is_private': chat.is_private,
            'status': 'created'
        })

    def delete(self, chat_id):
        self.abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        session.delete(chat)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_chat_not_found(self, chat_id):
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        if not chat:
            abort(404, message=f"Chat {chat_id} not found")


class MessageResource(Resource):
    def get(self, chat_id):
        self.abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        messages = session.query(Message).filter_by(chat_id=chat_id).limit(100).all()

        result = []
        for msg in messages:
            sender = session.get(User, msg.sender_id)

            #  Конвертируем бинарное фото из БД в base64 для фронтенда
            picture_uri = None
            if msg.picture:
                picture_uri = f"data:image/jpeg;base64,{base64.b64encode(msg.picture).decode()}"

            result.append({
                'id': msg.id,
                'content': msg.content,
                'timestamp': msg.timestamp,
                'sender_id': msg.sender_id,
                'sender_name': sender.username if sender else 'Unknown',
                'picture': picture_uri
            })
        return jsonify({'messages': result})

    def post(self, chat_id):
        self.abort_if_chat_not_found(chat_id)
        args = message_parser.parse_args()
        session = db_session.create_session()
        picture_bytes = None
        if args.get('picture'):
            pic_str = args['picture']
            if pic_str.startswith('data:'):
                pic_str = pic_str.split(',', 1)[1]
            picture_bytes = base64.b64decode(pic_str)
        message = Message(
            content=args['content'],
            chat_id=chat_id,
            sender_id=args['sender_id'],
            picture=picture_bytes,
            coordinates=args['coordinates']
        )
        session.add(message)
        session.commit()
        return jsonify({'message': message.to_dict(only=('content', 'timestamp'))})

    def delete(self, message_id):
        self.abort_if_message_not_found(message_id)
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        session.delete(message)
        session.commit()
        return jsonify({'success': 'OK'})

    def abort_if_chat_not_found(self, chat_id):
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        if not chat:
            abort(404, message=f"Chat {chat_id} not found")

    def abort_if_message_not_found(self, message_id):
        session = db_session.create_session()
        chat = session.query(Chat).get(message_id)
        if not chat:
            abort(404, message=f"Chat {message_id} not found")