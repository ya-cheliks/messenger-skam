from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from auth import auth  # абсолютный импорт
from models import db, User  # абсолютный импорт (убрали ..)


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

        if User.query.filter_by(username=username).first():
            flash('Такой пользователь уже есть!', 'error')
            return redirect(url_for('auth.register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь войдите.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('chat.index'))
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('auth.login'))