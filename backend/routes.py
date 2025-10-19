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
                flash("Please set your la first!")
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
                if phone and not user:
                    user = db.query(Senior).filter(Senior.phone == phone).first()
            finally:
                db.close()
            if user and check_password_hash(user.password_hash, password):
                session["user_id"] = user.id
                session["user_name"] = user.name
                session["user_role"] = "senior"
                return redirect(url_for("dashboard"))
            flash("Invalid credentials")
            return redirect(url_for("login_senior"))
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
                if phone and not caretaker:
                    caretaker = db.query(Caretaker).filter(Caretaker.phone == phone).first()
            finally:
                db.close()
            if caretaker and check_password_hash(caretaker.password_hash, password):
                session["user_id"] = caretaker.id
                session["user_name"] = caretaker.name
                session["user_role"] = "caretaker"
                return redirect(url_for("dashboard"))
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
    @login_required
    def dashboard():
        user_id = session.get("user_id")
        role = session.get("user_role")
        db = SessionLocal()
        try:
            if role == 'senior':
                user = db.query(Senior).filter_by(id=user_id).first()
                return render_template('dashboard_senior.html', user=user)
            elif role == 'caretaker':
                user = db.query(Caretaker).filter_by(id=user_id).first()
                requests = db.query(HelpRequest).options(joinedload(HelpRequest.senior)).all()
                data = [
                    {
                        "id": r.id,
                        "senior_id": r.senior_id,
                        "title": r.title,
                        "description": r.description,
                        "category": r.category,
                        "lat": r.lat,
                        "lng": r.lng,
                        "status": r.status,
                        "created_at": r.created_at,
                        "senior_name": r.senior.name
                    }
                    for r in requests
                ]
                accepted = db.query(Request).options(joinedload(Request.senior)).filter_by(caretaker_id=user_id).all()
                print("ACCEPTED:", accepted)
                atad = [
                    {
                        "id": r.id,
                        "senior_id": r.senior_id,
                        "title": r.title,
                        "description": r.description,
                        "category": r.category,
                        "lat": r.lat,
                        "lng": r.lng,
                        "status": r.status,
                        "caretaker_id": r.caretaker_id,
                        "senior_name": r.senior.name
                    }
                    for r in accepted
                ]
                return render_template('dashboard_caretaker.html', user=user, requests=data, accepted=atad)
        finally:
            db.close()
        return redirect('/login')


    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)

    @app.route("/users", methods=["GET"])
    def get_all_users():
        db = SessionLocal()
        try:
            seniors = db.query(Senior).all()
            caretakers = db.query(Caretaker).all()
            hr = db.query(HelpRequest).all()
            re = db.query(Request).all()
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
            ],
            "help_requests": [
                {
                    "id": r.id,
                    "senior_id": r.senior_id,
                    "title": r.title,
                    "description": r.description,
                    "category": r.category,
                    "lat": r.lat,
                    "lng": r.lng,
                    "status": r.status,
                    "created_at": r.created_at,
                    "time": r.time,
                }
                for r in hr
            ],
            "requests": [
                {
                    "id": r.id,
                    "senior_id": r.senior_id,
                    "title": r.title,
                    "description": r.description,
                    "category": r.category,
                    "lat": r.lat,
                    "lng": r.lng,
                    "status": r.status,
                    "caretaker_id": r.caretaker_id,
                    "time": r.time,
                }
                for r in re
            ]        }
        return jsonify(data)

    @app.route("/request_help", methods=["GET", "POST"])
    @login_required
    @location_required
    def request_help():
        user_id = session.get("user_id")
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            category = request.form.get("category")
            db = SessionLocal()
            req = db.query(Senior).filter_by(id=user_id).first()
            lat = req.lat
            lng = req.lng
            if not title or not description or not category or not lat or not lng:
                flash("All fields are required!")
                return redirect(url_for("request_help"))
            db = SessionLocal()
            try:
                help_request = HelpRequest(
                    senior_id=user_id,
                    title=title,
                    description=description,
                    category=category,
                    lat=lat,
                    lng=lng
                )
                db.add(help_request)
                db.commit()
            finally:
                db.close()
            flash("Your help request has been submitted!")
            return redirect(url_for("dashboard"))
        db = SessionLocal()
        user = db.query(Senior).filter_by(id=user_id).first()
        return render_template("request_help.html", user=user)

    @app.route("/set_location", methods=["GET", "POST"])
    @login_required
    def set_location():
        user_id = session.get("user_id")
        db = SessionLocal()
        try:
            user = db.query(Senior).filter_by(id=user_id).first()
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
        user = db.query(Senior).filter_by(id=user_id).first()
        return render_template("set_location.html", user=user)

    @app.route('/get_senior', methods=['POST'])
    def get_senior():
        senior_id = request.json.get('id')
        db = SessionLocal()
        try:
            senior = db.query(Senior).filter_by(id=senior_id).first()
            if not senior:
                return jsonify({"error": "Senior not found"}), 404
            return jsonify({"name": senior.name, "age": senior.age, "email": senior.email, "phone": senior.phone})
        finally:
            db.close()

    @app.route('/accept_request', methods=['POST'])
    def accept_request():
        id = request.form.get("id")
        db = SessionLocal()
        req = db.query(HelpRequest).filter_by(id=id).first()
        #First we need to create a item in the database Request with the information from the item in HelpRequest
        new_user = Request(
            senior_id=req.senior_id,
            title=req.title,
            description=req.description,
            category=req.category,
            lat=req.lat,
            lng=req.lng,
            caretaker_id=session.get("user_id"),
            time=req.time,
        )
        db.add(new_user)
        db.delete(req)
        db.commit()
        db.close()
        return redirect(url_for('dashboard'))

