from flask import Flask
from . import routes
from backend.db import Base, engine

def create_app():
    app = Flask("amogus", static_folder="frontend", template_folder="frontend")
    Base.metadata.create_all(bind=engine)
    app.secret_key = "fjshgisbcmzowhtidia"  # Replace with a secure key in production
    routes.init_app(app)
    return app
