from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from chat import chat
from data import db_session
from data.model_chat import Chat
from data.model_message import Message


@chat.route('/')
@login_required
def index():
    """Страница со списком чатов"""
    return render_template('chat/index.html')


@chat.route('/<int:chat_id>')
@login_required
def view(chat_id):
    """Страница просмотра конкретного чата"""
    session = db_session.create_session()
    chat_obj = session.query(Chat).get(chat_id)

    # Проверка: пользователь должен быть участником чата
    if not chat_obj:
        flash('Чат не найден', 'error')
        return redirect(url_for('chat.index'))

    # Простая проверка доступа (в реальном проекте — строже)
    users_list = chat_obj.users_id.split() if chat_obj.users_id else []
    if str(current_user.id) not in users_list and not chat_obj.is_private == False:
        flash('У вас нет доступа к этому чату', 'error')
        return redirect(url_for('chat.index'))

    session.close()

    return render_template('chat/view.html',
                           chat_id=chat_id,
                           chat_name=chat_obj.name)


@chat.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    """API для отправки сообщения (дополнительный эндпоинт)"""
    data = request.get_json()

    if not data or 'chat_id' not in data or 'content' not in data:
        return jsonify({'error': 'Некорректные данные'}), 400

    session = db_session.create_session()

    message = Message(
        content=data['content'],
        chat_id=data['chat_id'],
        sender_id=current_user.id
    )

    session.add(message)
    session.commit()

    result = {'id': message.id, 'status': 'sent'}
    session.close()

    return jsonify(result), 201