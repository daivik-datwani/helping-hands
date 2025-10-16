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
        # after successful signup, redirect to the login page
        return redirect(url_for('login'))
    
    @app.route("/signup.html")
    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/signup_senior")
    @app.route("/signup_senior.html")
    def signup_senior():
        return render_template("signup_senior.html")

    @app.route("/signup_caretaker")
    @app.route("/signup_caretaker.html")
    def signup_caretaker():
        return render_template("signup_caretaker.html")

    @app.route("/caretakers", methods=["POST"])
    def post_caretaker():
        name = request.form.get("name")
        age = request.form.get("age")
        phoneemail = request.form.get("phoneemail")
        session = SessionLocal()
        new_c = Caretaker(name=name, age=age, phoneemail=phoneemail)
        session.add(new_c)
        session.commit()
        session.close()
        return redirect(url_for('login_caretaker'))

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

    @app.route('/login_senior', methods=["GET", "POST"])
    def login_senior():
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('login_senior.html')

    @app.route('/login_caretaker', methods=["GET", "POST"])
    def login_caretaker():
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('login_caretaker.html')

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)

