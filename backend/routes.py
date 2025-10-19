from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior, Caretaker
from werkzeug.security import generate_password_hash, check_password_hash
from backend.helpers import *

def init_app(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/signup")
    @app.route("/signup.html")
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

    @app.route("/login")
    @app.route("/login.html")
    def login():
        return render_template("login.html")

    @app.route("/login_senior", methods=["GET", "POST"])
    def login_senior():
        if request.method == "POST":
            contact = request.form.get("email")
            password = request.form.get("password")
            db = SessionLocal()
            try:
                user = None
                if contact:
                    # Check both email and phone
                    user = db.query(Senior).filter(
                        (Senior.email == contact) | (Senior.phone == contact)
                    ).first()
            finally:
                db.close()

            if user and check_password_hash(user.password_hash, password):
                session["user_id"] = user.id
                session["user_name"] = user.name
                return redirect(url_for("dashboard"))
            flash("Invalid credentials")
            return redirect(url_for("login_senior"))
        return render_template("login_senior.html")

    @app.route("/login_caretaker", methods=["GET", "POST"])
    def login_caretaker():
        if request.method == "POST":
            contact = request.form.get("email")
            password = request.form.get("password")
            db = SessionLocal()
            try:
                caretaker = None
                if contact:
                    caretaker = db.query(Caretaker).filter(
                        (Caretaker.email == contact) | (Caretaker.phone == contact)
                    ).first()
            finally:
                db.close()

            if caretaker and check_password_hash(caretaker.password_hash, password):
                session["user_id"] = caretaker.id
                session["user_name"] = caretaker.name
                return redirect(url_for("home"))
            flash("Invalid credentials")
            return redirect(url_for("login_caretaker"))
        return render_template("login_caretaker.html")

    @app.route("/users", methods=["POST"])
    def signup_senior_post():
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not name or not password or (not email and not phone):
            flash("All fields are required.")
            return redirect(url_for("signup_senior"))

        hashed_password = generate_password_hash(password)
        db = SessionLocal()
        new_user = Senior(
            name=name,
            age=age,
            email=email if email else None,
            phone=phone if phone else None,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.close()
        flash("Signup successful! Please log in.")
        return redirect(url_for("login_senior"))

    @app.route("/caretakers", methods=["POST"])
    def signup_caretaker_post():
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not name or not password or (not email and not phone):
            flash("All fields are required.")
            return redirect(url_for("signup_caretaker"))

        hashed_password = generate_password_hash(password)
        db = SessionLocal()
        new_user = Caretaker(
            name=name,
            age=age,
            email=email if email else None,
            phone=phone if phone else None,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.close()
        flash("Signup successful! Please log in.")
        return redirect(url_for("login_caretaker"))

    @app.route('/dashboard')
    def dashboard():
        username = session.get("user_name")
        if not username:
            return redirect('/login')
        return render_template('dashboard.html', name=username)

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)
    @app.route("/users", methods=["GET"])
    def get_all_users():
        db = SessionLocal()
        try:
            seniors = db.query(Senior).all()
            caretakers = db.query(Caretaker).all()
        finally:
            db.close()

        data = {
            "seniors": [
                {
                    "id": s.id,
                    "name": s.name,
                    "age": s.age,
                    "email": s.email,
                    "phone": s.phone,
                    "password_hash": s.password_hash
                }
                for s in seniors
            ],
            "caretakers": [
                {
                    "id": c.id,
                    "name": c.name,
                    "age": c.age,
                    "email": c.email,
                    "phone": c.phone,
                    "password_hash": c.password_hash
                }
                for c in caretakers
            ]
        }
        return jsonify(data)