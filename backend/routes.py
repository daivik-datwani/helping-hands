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
        data = [{"Senior": u.name, "Age": u.age, "Email": u.email, "Phone": u.phone, "Password": u.password} for u in users]
        return jsonify(data)

    @app.route("/users", methods=["POST"])
    def post_data():
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        session = SessionLocal()
        new_user = User(name=name, age=age, email=email, phone=phone, password=password)
        session.add(new_user)
        session.commit()
        session.close()
        # after successful signup, redirect to the login page
        return redirect(url_for('login'))
    
    @app.route("/signup.html")
    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/login.html")
    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login_post():
        # Very small placeholder login handler. In production, validate credentials.
        email = request.form.get('email')
        # For now, just redirect to home after "login" to avoid 404s.
        return redirect(url_for('home'))

    # this code makes url allow no file extension
    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)

