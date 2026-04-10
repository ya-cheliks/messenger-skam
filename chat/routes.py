import requests
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from chat import chat

API_URL = 'http://127.0.0.1:5000'


@chat.route('/')
@login_required
def index():
    try:
        response = requests.get(f'{API_URL}/api/users/{current_user.id}')
        chats = response.json().get('chats', []) if response.status_code == 200 else []
    except Exception:
        chats = []
    return render_template('chat/index.html', chats=chats)


@chat.route('/<int:chat_id>')
@login_required
def view(chat_id):
    try:
        response = requests.get(f'{API_URL}/api/users/{current_user.id}')
        if response.status_code != 200:
            flash('Ошибка загрузки данных', 'error')
            return redirect(url_for('chat.index'))

        target_chat = next((c for c in response.json().get('chats', []) if c.get('id') == chat_id), None)
        if not target_chat:
            flash('Чат не найден', 'error')
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
    try:
        resp = requests.get(f'{API_URL}/api/chats/messages/{chat_id}')
        return jsonify(resp.json() if resp.status_code == 200 else {'messages': []}), 200
    except Exception:
        return jsonify({'messages': []}), 200


@chat.route('/api/messages', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    if not data or 'chat_id' not in data or 'content' not in data:
        return jsonify({'error': 'Некорректные данные'}), 400

    try:
        payload = {
            'content': data['content'].strip(),
            'chat_id': data['chat_id'],
            'sender_id': current_user.id,
            'picture': data.get('picture'),
            'coordinates': None
        }
        resp = requests.post(f'{API_URL}/api/chats/messages/{data["chat_id"]}', json=payload)
        return jsonify(
            {'status': 'sent'} if resp.status_code in [200, 201] else {'error': 'API Error'}), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat.route('/api/avatar/<int:user_id>', methods=['GET'])
@login_required
def get_avatar(user_id):
    try:
        resp = requests.get(f'{API_URL}/api/users/{user_id}')
        if resp.status_code == 200:
            avatar = resp.json().get('user', {}).get('avatar')
            return jsonify({'avatar': avatar}), 200
        return jsonify({'avatar': None}), 200
    except Exception:
        return jsonify({'avatar': None}), 200


@chat.route('/api/avatar', methods=['POST'])
@login_required
def upload_avatar():
    try:
        data = request.get_json()
        if not data or 'avatar' not in data:
            return {'error': 'Нет данных'}, 400

        resp = requests.patch(f'{API_URL}/api/users/{current_user.id}', json={'avatar': data['avatar']})
        return jsonify(resp.json() if resp.status_code in [200, 201] else {'error': 'API Error'}), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500