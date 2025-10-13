from flask import Flask
from . import routes

def create_app():
    app = Flask("amogus", template_folder="frontend")
    routes.init_app(app)
    return app
