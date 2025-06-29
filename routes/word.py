from flask import Blueprint, render_template, request, jsonify
from services.word_service import get_word_list
import os
from werkzeug.utils import secure_filename

# Create a Blueprint for word-related routes
word_bp = Blueprint("word", __name__)

# Set upload folder path and ensure it exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@word_bp.route("/")
def record_words():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Render the main page for word-by-word recording.

    Args:
        None (GET request)
    Returns:
        Rendered word_record.html template with word list.
    """
    # Get the list of words to record
    words = get_word_list()

    return render_template("word_record.html", words=words)


@word_bp.route("/upload", methods=["POST"])
def upload_audio():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Save the uploaded audio file from the browser to the server.

    Args:
        audio: Uploaded audio file (multipart/form-data)
        word: The word for which the audio was recorded (form field)
    Returns:
        JSON (success status, saved filename)
    """
    # Check if both audio file and word are provided in the request
    if "audio" not in request.files or "word" not in request.form:
        return (
            jsonify(
                {"success": False, "error": "단어나 오디오 파일이 변형되었습니다."}
            ),
            400,
        )

    audio = request.files["audio"]
    word = request.form["word"]

    # Create a secure filename for saving
    filename = secure_filename(f"{word}_{audio.filename}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the audio file to the uploads folder
    audio.save(save_path)

    return jsonify({"success": True, "filename": filename})
