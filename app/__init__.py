from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_uploads import configure_uploads, UploadSet

moment = Moment()
db = SQLAlchemy()
photos = UploadSet('PHOTO')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)

    @app.route('/')
    def index():
        return '<h1>Hello World!</h1>'

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    return app
