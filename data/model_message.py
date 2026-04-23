import sqlalchemy, datetime
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('chats.id'), index=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    picture = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    coordinates = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)

    def __repr__(self):
        return f'<Message> {self.id} for Chat {self.chat_id}'
