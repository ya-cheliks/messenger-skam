from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from chat import chat

@chat.route('/')
@login_required
def index():
    return render_template('chat/index.html')