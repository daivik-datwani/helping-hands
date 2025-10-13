from flask import render_template

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')
