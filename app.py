import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db
from routes.word import word_bp
from routes.admin import admin_bp

load_dotenv()  # .env 파일에서 환경변수 로드

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(word_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
