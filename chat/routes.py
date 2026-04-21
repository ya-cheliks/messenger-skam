# chat/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import chat
from data import db_session
from data.model_user import User
from data.model_chat import Chat
from data.model_message import Message
import base64


@chat.route('/')
@login_required
def index():
    session = db_session.create_session()
    try:
        all_chats = session.query(Chat).all()
        user_chats = [
            c for c in all_chats
            if str(current_user.id) in (c.users_id or '').split()
        ]
        chats_data = [c.to_dict(only=('id', 'name', 'is_private')) for c in user_chats]
    finally:
        session.close()
    return render_template('chat/index.html', chats=chats_data)


@chat.route('/<int:chat_id>')
@login_required
def view(chat_id):
    session = db_session.create_session()
    try:
        chat_obj = session.get(Chat, chat_id)
        if not chat_obj or str(current_user.id) not in (chat_obj.users_id or '').split():
            flash('Чат не найден или нет доступа', 'error')
            return redirect(url_for('chat.index'))

        messages = session.query(Message).filter_by(chat_id=chat_id).order_by(Message.timestamp.asc()).all()

        rendered_msgs = []
        for msg in messages:
            sender = session.get(User, msg.sender_id)
            pic_uri = None
            if msg.picture:
                pic_uri = f"data:image/jpeg;base64,{base64.b64encode(msg.picture).decode()}"

            rendered_msgs.append({
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M') if msg.timestamp else '',
                'sender_name': sender.username if sender else 'Unknown',
                'is_mine': msg.sender_id == current_user.id,
                'picture': pic_uri
            })

        return render_template('chat/view.html',
                               chat_id=chat_id,
                               chat_name=chat_obj.name,
                               messages=rendered_msgs)
    finally:
        session.close()


@chat.route('/<int:chat_id>/send', methods=['POST'])
@login_required
def send_message(chat_id):
    content = request.form.get('content', '').strip()
    photo_file = request.files.get('photo')

    picture_bytes = None
    if photo_file and photo_file.filename:
        if photo_file.content_type.startswith('image/'):
            picture_bytes = photo_file.read()
        else:
            flash('Поддерживаются только изображения', 'warning')
            return redirect(url_for('chat.view', chat_id=chat_id))

    if not content and not picture_bytes:
        flash('Сообщение не может быть пустым', 'warning')
        return redirect(url_for('chat.view', chat_id=chat_id))

    session = db_session.create_session()
    try:
        new_msg = Message(
            content=content,
            chat_id=chat_id,
            sender_id=current_user.id,
            picture=picture_bytes
        )
        session.add(new_msg)
        session.commit()
    except Exception:
        session.rollback()
        flash('Ошибка при отправке сообщения', 'error')
    finally:
        session.close()

    return redirect(url_for('chat.view', chat_id=chat_id))