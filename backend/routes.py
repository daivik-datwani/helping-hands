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
            user = None
            if "@" in contact:
                user = db.query(Senior).filter_by(email=contact).first()
            else:
                user = db.query(Senior).filter_by(phone=contact).first()
            db.close()
            if user and check_password_hash(user.password_hash, password):
                session["user_id"] = user.id
                session["user_name"] = user.name
                return redirect(url_for("home"))
            flash("Invalid credentials")
            return redirect(url_for("login_senior"))
        return render_template("login_senior.html")

    @app.route("/login_caretaker", methods=["GET", "POST"])
    def login_caretaker():
        if request.method == "POST":
            contact = request.form.get("email")
            password = request.form.get("password")
            db = SessionLocal()
            user = None
            if "@" in contact:
                user = db.query(Caretaker).filter_by(email=contact).first()
            else:
                user = db.query(Caretaker).filter_by(phone=contact).first()
            db.close()
            if user and check_password_hash(user.password_hash, password):
                session["user_id"] = user.id
                session["user_name"] = user.name
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
        new_user = Senior(name=name, age=age, email=email if email else None, phone=phone if phone else None, password_hash=hashed_password)
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
        new_user = Caretaker(name=name, age=age, email=email if email else None, phone=phone if phone else None, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.close()
        flash("Signup successful! Please log in.")
        return redirect(url_for("login_caretaker"))

        session = SessionLocal()
        new_c = Caretaker(name=name, age=age, email=email, phone=phone, password=password)
        session.add(new_c)
        session.commit()
        session.close()
        # after successful signup, redirect to the login page
        return redirect(url_for('login_caretaker'))

    @app.route('/login_senior', methods=["GET", "POST"])
    def login_senior():
        if request.method == 'POST':
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")
            session = SessionLocal()
            try:
                user = None
                if email:
                    user = session.query(User).filter_by(email=email).first()
                if not user and phone:
                    user = session.query(User).filter_by(phone=phone).first()
            finally:
                session.close()
            if user and user.password == password:
                return redirect(url_for('home')) #change to dashboard later
            return render_template('login_senior.html', error="Invalid email or password")
        return render_template('login_senior.html')

    @app.route('/login_caretaker', methods=["GET", "POST"])
    def login_caretaker():
        if request.method == 'POST':
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")
            session = SessionLocal()
            try:
                cs = session.query(Caretaker).filter_by(email=email).first()
            except:
                try:
                    cs = session.query(Caretaker).filter_by(phone=phone).first()
                finally:
                    session.close()
            finally:
                session.close()
            if cs and cs.password == password:
                return redirect(url_for('home')) #change to dashboard later
            return render_template('login_caretaker.html')
        return render_template('login_caretaker.html')

    # this code makes url allow no file extension

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)
