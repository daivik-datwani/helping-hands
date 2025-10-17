from flask import *
from backend.db import SessionLocal
from backend.models.helpinghandsdatabase import Senior as User
from backend.models.helpinghandsdatabase import Caretaker as Caretaker
from backend.models.helpinghandsdatabase import Request as RequestModel  

def init_app(app):
    @app.route("/")
    def home():
        return render_template("index.html")

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

    @app.route("/login.html")
    @app.route("/login")
    def login():
        return render_template("login.html")
    
    @app.route("/users", methods=["GET"])
    def get_seniors():
        session = SessionLocal()
        try:
            users = session.query(User).all()
        finally:
            session.close()
        data = [{"Senior": u.name, "Age": u.age, "Email": u.email, "Phone": u.phone, "Password": u.password} for u in users]
        return jsonify(data)

    @app.route("/users", methods=["POST"])
    def post_seniors():
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
        return redirect(url_for('login_senior'))

    @app.route("/caretakers", methods=["GET"])
    def get_cs():
        session = SessionLocal()
        try:
            cs = session.query(Caretaker).all()
        finally:
            session.close()
        data = [{"Caretaker": u.name, "Age": u.age, "Email": u.email, "Phone": u.phone, "Password": u.password} for u in cs]
        return jsonify(data)
    
    @app.route("/caretakers", methods=["POST"])
    def post_cs():
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

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
            password = request.form.get("password")
            session = SessionLocal()
            try:
                user = session.query(User).filter_by(email=email).first()
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
            password = request.form.get("password")
            session = SessionLocal()
            try:
                cs = session.query(Caretaker).filter_by(email=email).first()
            finally:
                session.close()
            if cs and cs.password == password:
                return redirect(url_for('home')) #change to dashboard later
            return render_template('login_caretaker.html', error="Invalid email or password")
        return render_template('login_caretaker.html')

    # this code makes url allow no file extension
    @app.route("/<path:filename>")
    def serve_static(filename):
        return send_from_directory('frontend', filename)

