from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Импорт routes после создания blueprint
from . import routes