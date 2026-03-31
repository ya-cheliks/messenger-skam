from flask_restful import reqparse, abort, Resource
from data import db_session
from flask import jsonify
from werkzeug.security import generate_password_hash
from data.model_user import User
from data.model_chat import Chat
from data.model_message import Message
from api import user_parser, chat_parser


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
        print(args)
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
    def get(self, chat_id):
        self.abort_if_chat_not_found(chat_id)
        session = db_session.create_session()
        chat = session.query(Chat).get(chat_id)
        # Получаем последние 100 сообщений чата
        messages = session.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.timestamp.desc()).limit(100).all()

        return jsonify({
            'chat': chat.to_dict(only=('id', 'name', 'is_private', 'created_at')),
            'users_count': len([int(uid) for uid in chat.users_id.split() if uid]),
            'messages': [msg.to_dict(only=('id', 'content', 'sender_id', 'timestamp'))
                         for msg in messages]
        })

    def post(self):
        args = chat_parser.parse_args()  # name, users_id="1 2 3", is_private
        session = db_session.create_session()
        chat = Chat(
            name=args['name'],
            users_id=args['users_id'],  # "1 2 3"
            is_private=args.get('is_private', False)  #
        )
        session.add(chat)
        session.commit()
        return jsonify({
            'id': chat.id,
            'name': chat.name,
            'is_private': chat.is_private,
            'status': 'created'
        }), 201

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