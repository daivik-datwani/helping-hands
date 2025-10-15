from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior as User
from backend.models.helpinghandsdatabase import Caretaker as Caretaker
from backend.models.helpinghandsdatabase import Request as RequestModel  

def init_app(app):
    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route("/users", methods=["GET"])
    def get_data():
        session = SessionLocal()
        try:
            users = session.query(User).all()
        finally:
            session.close()
        data = [{"Senior": u.name, "Age": u.age, "Contact": u.phoneemail} for u in users]
        return jsonify(data)

    @app.route("/users", methods=["POST"])
    def post_data():
        name = request.form.get("name")
        age = request.form.get("age")
        phoneemail = request.form.get("phoneemail")

        session = SessionLocal()
        new_user = User(name=name, age=age, phoneemail=phoneemail)
        session.add(new_user)
        session.commit()
        session.close()
        return "<script>alert('success!!'); window.location.href='/signup';</script>"
    
    @app.route("/signup.html")
    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/login.html")
    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)

