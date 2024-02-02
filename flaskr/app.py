import os

from flask import Flask
from .routes import configure_routes
def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = int(os.environ.get('FLASK_DEBUG', '0')) == 1

    configure_routes(app)
    return app