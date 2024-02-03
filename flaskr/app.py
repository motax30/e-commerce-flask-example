from flask import Flask
from . import routes
from . import db
from . import config_app

def create_app():
    app = Flask(__name__)
    
    config_app.init_app(app)
    db.init_app(app)
    routes.configure_routes(app)
    
    return app