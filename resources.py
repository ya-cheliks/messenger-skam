from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from flask import jsonify
from werkzeug.security import generate_password_hash
from data.users_model import User
from data.chats_model import Chat
from data.messages_model import Messages
from api import parser


class UserResource(Resource):
    def get(self, user_id):
        self.abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        # chats_id парсим как список ID
        chat_ids = [int(cid) for cid in user.chats_id.split() if cid]
        chats = [session.get(Chat, cid) for cid in chat_ids if session.get(Chat, cid)]
        return jsonify({
            'user': user.to_dict(only=('id', 'username', 'avatar')),
            'chats': [chat.to_dict(only=('id', 'name')) for chat in chats]
        })

    def post(self):
        args = parser.parse_args()  # username, password
        session = db_session.create_session()
        user = User(
            username=args['username'],
            password_hash=generate_password_hash(args['password'])
        )
        session.add(user)
        session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'status': 'registered'
        }), 201

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
        messages = session.query(Messages).filter(
            Messages.chat_id == chat_id
        ).order_by(Messages.timestamp.desc()).limit(100).all()

        return jsonify({
            'chat': chat.to_dict(only=('id', 'name', 'is_private', 'created_at')),
            'users_count': len([int(uid) for uid in chat.users_id.split() if uid]),
            'messages': [msg.to_dict(only=('id', 'content', 'sender_id', 'timestamp'))
                         for msg in messages]
        })

    def post(self):
        args = parser.parse_args()  # name, users_id="1 2 3", is_private
        session = db_session.create_session()
        chat = Chat(
            name=args['name'],
            users_id=args['users_id'],  # "1 2 3"
            is_private=args.get('is_private', True)
        )
        session.add(chat)
        session.commit()
        return jsonify({
            'id': chat.id,
            'name': chat.name,
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