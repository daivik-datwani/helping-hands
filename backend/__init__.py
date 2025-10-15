from flask import Flask
from . import routes
from backend.db import Base, engine

def create_app():
    app = Flask("amogus", static_folder="frontend", template_folder="frontend")
    Base.metadata.create_all(bind=engine)
    routes.init_app(app)
    return app
