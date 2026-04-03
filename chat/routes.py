import requests
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from chat import chat

API_URL = 'http://127.0.0.1:5000'


@chat.route('/')
@login_required
def index():
    """Страница со списком чатов (данные берём через API)"""
    try:
        response = requests.get(f'{API_URL}/api/users/{current_user.id}')
        if response.status_code == 200:
            data = response.json()
            chats = data.get('chats', [])
        else:
            chats = []
    except Exception:
        chats = []

    return render_template('chat/index.html', chats=chats)


@chat.route('/<int:chat_id>')
@login_required
def view(chat_id):
    """Страница просмотра чата (проверка доступа через API)"""
    try:
        response = requests.get(f'{API_URL}/api/users/{current_user.id}')
        if response.status_code != 200:
            flash('Ошибка загрузки данных', 'error')
            return redirect(url_for('chat.index'))

        user_data = response.json()
        chats_list = user_data.get('chats', [])

        target_chat = None
        for c in chats_list:
            if c.get('id') == chat_id:
                target_chat = c
                break

        if not target_chat:
            flash('Чат не найден или нет доступа', 'error')
            return redirect(url_for('chat.index'))

        return render_template('chat/view.html',
                               chat_id=chat_id,
                               chat_name=target_chat.get('name', 'Чат'))

    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('chat.index'))


@chat.route('/api/messages/<int:chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    """Промежуточный эндпоинт для получения сообщений через API"""
    try:
        response = requests.get(f'{API_URL}/api/chats/messages/{chat_id}')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({'messages': []}), 200
    except Exception:
        return jsonify({'messages': []}), 200


@chat.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    """Промежуточный эндпоинт для отправки сообщений через API"""
    data = request.get_json()
    # ✅ ИСПРАВЛЕНО: добавлено "data:" в конце условия
    if not data or 'chat_id' not in data or 'content' not in data:
        return jsonify({'error': 'Некорректные данные'}), 400

    chat_id = data['chat_id']
    content = data['content'].strip()
    if not content:
        return jsonify({'error': 'Пустое сообщение'}), 400

    try:
        payload = {
            'content': content,
            'chat_id': chat_id,
            'sender_id': current_user.id
        }
        response = requests.post(f'{API_URL}/api/chats/messages/{chat_id}', json=payload)

        if response.status_code in [200, 201]:
            return jsonify({'status': 'sent', 'data': response.json()}), 201
        return jsonify({'error': 'Ошибка API'}), 500
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500