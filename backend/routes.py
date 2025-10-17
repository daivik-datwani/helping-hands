from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior as User
from backend.models.helpinghandsdatabase import Caretaker as Caretaker
from backend.models.helpinghandsdatabase import Request as RequestModel  
from werkzeug.security import generate_password_hash, check_password_hash
from backend.helpers import *

def init_app(app):
    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route("/users", methods=["GET"])
    def get_users():
        db = SessionLocal()
        try:
            users = db.query(User).all()
            data = [{"Senior": u.name, "Age": u.age, "Contact": u.phone or u.email} for u in users]
            return jsonify(data)
        finally:
            db.close()

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template("signup.html")

        name = request.form.get("name")
        age = request.form.get("age")
        phoneemail = request.form.get("phoneemail")
        password = request.form.get("password")

        if not name or not password or not phoneemail:
            flash("All fields are required.")
            return redirect(url_for("signup"))

        email = None
        phone = None
        if is_email(phoneemail):
            email = phoneemail
        elif is_phone(phoneemail):
            phone = phoneemail
        else:
            flash("Please enter a valid email or phone number.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        db = SessionLocal()
        if phone:
            new_user = User(name=name, age=age, phone=phone, password_hash=hashed_password)
        else:
            new_user = User(name=name, age=age, email=email, password_hash=hashed_password)

        db.add(new_user)
        db.commit()
        db.close()

        flash("Signup successful! Please log in.")
        return redirect(url_for("login"))
    
    @app.route("/login.html")
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            contact = request.form.get("contact")
            password = request.form.get("password")

            db = SessionLocal()
            user = None
            if "@" in contact:
                user = db.query(User).filter_by(email=contact).first()
            else:
                user = db.query(User).filter_by(phone=contact).first()
            db.close()

            if user and check_password_hash(user.password_hash, password):
                session["user_id"] = user.id
                session["user_name"] = user.name # lets think about how long we want to keep this session data
                return redirect(url_for("home"))
            else:
                flash("Invalid credentials") # ig we can do this for now but lets make a nicer UI later
                return redirect(url_for("login"))

        return render_template("login.html")

    # @app.route("/login", methods=["POST"])
    # def login_post():
    #     # Very small placeholder login handler. In production, validate credentials.
    #     email = request.form.get('email')
    #     # For now, just redirect to home after "login" to avoid 404s.
    #     return redirect(url_for('home'))

    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)
