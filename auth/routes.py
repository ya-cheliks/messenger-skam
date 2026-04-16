import requests
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from data import db_session
from data.model_user import User
import os

API_URL = os.getenv('API_URL', 'http://127.0.0.1:5000')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not username or not password:
            flash('Заполните все поля!', 'error')
            return redirect(url_for('auth.register'))

        if password != password2:
            flash('Пароли не совпадают!', 'error')
            return redirect(url_for('auth.register'))

        # --- Регистрация через API ---
        try:
            response = requests.post(f'{API_URL}/api/users', json={
                'username': username,
                'password': password
            })

            if response.status_code in [200, 201]:
                flash('Регистрация прошла успешно! Теперь войдите.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Ошибка регистрации (возможно, пользователь уже существует)', 'error')

        except requests.exceptions.ConnectionError:
            flash('Не удалось подключиться к API', 'error')

        return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        session = db_session.create_session()
        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('chat.index'))
        else:
            flash('Неверный логин или пароль', 'error')
        session.close()

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('auth.login'))