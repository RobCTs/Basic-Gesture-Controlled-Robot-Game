from flask import Flask
from flask_wtf import CSRFProtect

# Creates the Tablet Flask app
def create_app():
    # Create the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hri_project'

    # Initialize the CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Register the blueprints
    from apps.home.views import home
    app.register_blueprint(home) # Home blueprint

    from apps.game.views import game
    app.register_blueprint(game) # Game blueprint

    from apps.robot.views import robot
    app.register_blueprint(robot) # Robot blueprint

    return app

