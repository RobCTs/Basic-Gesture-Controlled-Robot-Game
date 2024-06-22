from flask import Flask
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hri_project'

    csrf = CSRFProtect()
    csrf.init_app(app)

    from apps.home.views import home
    app.register_blueprint(home)

    from apps.game.views import game
    app.register_blueprint(game)

    return app

