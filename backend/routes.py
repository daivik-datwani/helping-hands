from flask import *
from backend.db import SessionLocal
from backend.models.thedatabaseidk import Senior as User
from backend.models.thedatabaseidk import Caretaker as Caretaker
from backend.models.thedatabaseidk import Request as RequestModel  

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/users', methods=['GET'])
    def get_data():
        session = SessionLocal()
        try:
            users = session.query(User).all()
        finally:
            session.close()
        data = [{"Senior": u.name, "Age": u.age, "Contact": u.phoneemail} for u in users]
        return jsonify(data)
    
    @app.route('/users', methods=['POST'])
    def post_data():
        data = request.get_json()
        session = SessionLocal()
        new_user = User(
            name=data.get("Senior"),
            age=data.get("Age"),
            phoneemail=data.get("Contact")
        )
        session.add(new_user)
        session.commit()
        session.close()
        return jsonify({"status": "success :)"})
