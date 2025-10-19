from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior, Caretaker, HelpRequest, Request
from werkzeug.security import generate_password_hash, check_password_hash
from backend.helpers import *
from sqlalchemy.orm import joinedload

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
                    user = db.query(Senior).filter(
                        (Senior.email == email)
                    ).first()
                if phone and not user:
                    user = db.query(Senior).filter(
                        (Senior.phone == phone)
                    ).first()
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
                    caretaker = db.query(Caretaker).filter(
                        (Caretaker.email == email)
                    ).first()
                if phone and not caretaker:
                    caretaker = db.query(Caretaker).filter(
                        (Caretaker.phone == phone)
                    ).first()
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
    def dashboard():
        user_id = session.get("user_id")
        if not user_id:
            return redirect('/login')
        db = SessionLocal()
        if session.get('user_role') == 'senior':
            user = db.query(Senior).filter_by(id=user_id).first()
            db.close()
            return render_template('dashboard_senior.html', user=user)
        elif session.get('user_role') == 'caretaker':
            user = db.query(Caretaker).filter_by(id=user_id).first()
            db.close()
            db = SessionLocal()
            try:
                requests = db.query(HelpRequest).options(joinedload(HelpRequest.senior)).all()
            finally:
                db.close()
            data = [
                {
                    "id": r.id,
                    "senior_id": r.senior_id,
                    "title": r.title,
                    "description": r.description,
                    "category": r.category,
                    "location": r.location,
                    "status": r.status,
                    "created_at": r.created_at,
                    "senior_name": r.senior.name
                }
                for r in requests
            ]
            db = SessionLocal()
            try:
                accepted = db.query(Request).options(joinedload(Request.senior)).filter_by(caretaker_id=user_id).all()
            finally:
                db.close()
            atad = [
                {
                    "id": r.id,
                    "senior_id": r.senior_id,
                    "title": r.title,
                    "description": r.description,
                    "category": r.category,
                    "location": r.location,
                    "status": r.status,
                    "caretaker_id": r.caretaker_id,
                    "senior_name": r.senior.name
                }
                for r in accepted
            ]

            return render_template('dashboard_caretaker.html', user=user, requests=data, accepted=atad)
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
                    "location": r.location,
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
                    "location": r.location,
                    "status": r.status,
                    "caretaker_id": r.caretaker_id,
                    "time": r.time,
                }
                for r in re
            ]        }
        return jsonify(data)

    @app.route("/request_help", methods=["GET", "POST"])
    def request_help():
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login_senior")
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            category = request.form.get("category")
            location = request.form.get("location")
            if not title or not description or not category or not location:
                flash("All fields are required!")
                return redirect(url_for("request_help"))
            db = SessionLocal()
            help_request = HelpRequest(
                senior_id=user_id,
                title=title,
                description=description,
                category=category,
                location=location
            )
            db.add(help_request)
            db.commit()
            db.close()
            flash("Your help request has been submitted!")
            return redirect(url_for("dashboard"))
        return render_template("request_help.html")

    @app.route('/get_senior', methods=['POST'])
    def get_senior():
        senior_id = request.json.get('id')
        db = SessionLocal()
        try:
            senior = db.query(Senior).filter_by(id=senior_id).first()
            if not senior:
                return jsonify({"error": "Senior not found"}), 404
            return jsonify({
                "name": senior.name,
                "age": senior.age,
                "email": senior.email,
                "phone": senior.phone
            })
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
            location=req.location,
            caretaker_id=session.get("user_id"),
            time=req.time,
        )
        db.add(new_user)
        db.delete(req)
        db.commit()
        db.close()
        return redirect(url_for('dashboard'))
