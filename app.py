from flask import Flask
from flask_cors import CORS

from config import Config
from models.setup import  db, Base
from models.models import  *
from blueprints.documents.documents_api import documents_api


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        # Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)
        # db.create_all()
    CORS(app)
    app.register_blueprint(documents_api)

    return app