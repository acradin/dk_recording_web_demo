import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db
from routes.instruction import instruction_bp
from routes.admin import admin_bp

load_dotenv()  # .env 파일에서 환경변수 로드

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

db.init_app(app)

app.register_blueprint(instruction_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
