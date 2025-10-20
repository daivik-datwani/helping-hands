from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior, Caretaker, HelpRequest, Request
from werkzeug.security import generate_password_hash, check_password_hash
from backend.helpers import *
from sqlalchemy.orm import joinedload
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("You need to log in first!")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def location_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = session.get("user_id")
        user_role = session.get("user_role")
        if not user_id or not user_role:
            flash("You need to log in first!")
            return redirect(url_for("login"))
        db = SessionLocal()
        try:
            user = None
            if user_role == "senior":
                user = db.query(Senior).filter_by(id=user_id).first()
            elif user_role == "caretaker":
                user = db.query(Caretaker).filter_by(id=user_id).first()
            if not user or user.lat is None or user.lng is None:
                flash("Please set your location first!")
                return redirect(url_for("set_location"))
        finally:
            db.close()
        return f(*args, **kwargs)
    return decorated

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

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/login")
    @app.route("/login.html")
    def login():
        return render_template("login.html")

    @app.route("/login_senior", methods=["GET", "POST"])
    def login_senior():
        if request.method == "POST":
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")

            db = SessionLocal()
            try:
                user = None
                if email:
                    user = db.query(Senior).filter(Senior.email == email).first()
                elif phone:
                    user = db.query(Senior).filter(Senior.phone == phone).first()

                if not user:
                    flash("Account not found.")
                    return redirect(url_for("login_senior"))

                if not check_password_hash(user.password_hash, password):
                    flash("Incorrect password.")
                    return redirect(url_for("login_senior"))

                session["user_id"] = user.id
                session["user_name"] = user.name
                session["user_role"] = "senior"
                return redirect(url_for("dashboard"))
            finally:
                db.close()

        return render_template("login_senior.html")

    @app.route("/login_caretaker", methods=["GET", "POST"])
    def login_caretaker():
        if request.method == "POST":
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")

            db = SessionLocal()
            try:
                caretaker = None
                if email:
                    caretaker = db.query(Caretaker).filter(Caretaker.email == email).first()
                elif phone:
                    caretaker = db.query(Caretaker).filter(Caretaker.phone == phone).first()

                if not caretaker:
                    flash("Account not found.")
                    return redirect(url_for("login_caretaker"))

                if not check_password_hash(caretaker.password_hash, password):
                    flash("Incorrect password.")
                    return redirect(url_for("login_caretaker"))

                session["user_id"] = caretaker.id
                session["user_name"] = caretaker.name
                session["user_role"] = "caretaker"
                return redirect(url_for("dashboard"))
            finally:
                db.close()

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

        db = SessionLocal()
        try:
            existing = db.query(Senior).filter(
                (Senior.email == email) | (Senior.phone == phone)
            ).first()
            if existing:
                flash("Account with this email or phone already exists.")
                return redirect(url_for("signup_senior"))

            hashed_password = generate_password_hash(password)
            new_user = Senior(
                name=name,
                age=age,
                email=email if email else None,
                phone=phone if phone else None,
                password_hash=hashed_password
            )
            db.add(new_user)
            db.commit()
        finally:
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
        try:
            new_user = Caretaker(
                name=name,
                age=age,
                email=email if email else None,
                phone=phone if phone else None,
                password_hash=hashed_password
            )
            db.add(new_user)
            db.commit()
        finally:
            db.close()

        flash("Signup successful! Please log in.")
        return redirect(url_for("login_caretaker"))

    @app.route('/dashboard')
    @login_required
    @location_required
    def dashboard():
        user_id = session.get("user_id")
        role = session.get("user_role")
        db = SessionLocal()
        try:
            if role == 'senior':
                requests = db.query(HelpRequest).all()
                accepted = db.query(Request).options(joinedload(Request.caretaker)).filter_by(senior_id=user_id).all()
                user = db.query(Senior).filter_by(id=user_id).first()
                return render_template('dashboard_senior.html', user=user, requests=requests, accepted=accepted)
            elif role == 'caretaker':
                user = db.query(Caretaker).filter_by(id=user_id).first()
                requests = db.query(HelpRequest).options(joinedload(HelpRequest.senior)).order_by(HelpRequest.created_at.desc()).all()
                accepted = db.query(Request).options(joinedload(Request.senior)).filter_by(caretaker_id=user_id).all()
                return render_template('dashboard_caretaker.html', user=user, requests=requests, accepted=accepted)
        finally:
            db.close()
        return redirect('/login')

    @app.route("/set_location", methods=["GET", "POST"])
    @login_required
    def set_location():
        user_id = session.get("user_id")
        role = session.get("user_role")
        db = SessionLocal()
        try:
            user = None
            if role == "senior":
                user = db.query(Senior).filter_by(id=user_id).first()
            elif role == "caretaker":
                user = db.query(Caretaker).filter_by(id=user_id).first()

            if request.method == "POST":
                lat = request.form.get("lat")
                lng = request.form.get("lng")
                if lat and lng:
                    user.lat = float(lat)
                    user.lng = float(lng)
                    db.commit()
                    flash("Location saved!")
                    return redirect(url_for("dashboard"))
        finally:
            db.close()
        return render_template("set_location.html", user=user)
