from flask import Blueprint, render_template, request, jsonify
from services.word_service import get_word_list
import os
from werkzeug.utils import secure_filename

word_bp = Blueprint("word", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@word_bp.route("/")
def record_words():
    words = get_word_list()
    return render_template("word_record.html", words=words)


@word_bp.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files or "word" not in request.form:
        return jsonify({"success": False, "error": "No audio or word provided"}), 400
    audio = request.files["audio"]
    word = request.form["word"]
    filename = secure_filename(f"{word}_{audio.filename}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(save_path)
    return jsonify({"success": True, "filename": filename})
