from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt, mail
from routes.auth import auth_bp
from routes.applications import app_bp
from routes.staff import staff_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(app_bp, url_prefix="/applications")
    app.register_blueprint(staff_bp, url_prefix="/staff")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
