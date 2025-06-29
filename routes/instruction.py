from flask import Blueprint, render_template, request, jsonify
from services.instruction_service import get_instruction_list
import os
from werkzeug.utils import secure_filename
from unidecode import unidecode

# Create a Blueprint for instruction-related routes
instruction_bp = Blueprint("instruction", __name__)

# Set upload folder path and ensure it exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@instruction_bp.route("/")
def record_instructions():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Render the main page for instruction-by-instruction recording.

    Args:
        None (GET request)
    Returns:
        Rendered instruction_record.html template with instruction list.
    """
    # Get the list of instructions to record
    instructions = get_instruction_list()

    return render_template("instruction_record.html", instructions=instructions)


@instruction_bp.route("/upload", methods=["POST"])
def upload_audio():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Save the uploaded audio file from the browser to the server.

    Args:
        audio: Uploaded audio file (multipart/form-data)
        instruction: The instruction for which the audio was recorded (form field)
    Returns:
        JSON (success status, saved filename)
    """
    # Check if both audio file and instruction are provided in the request
    if "audio" not in request.files or "instruction" not in request.form:
        return (
            jsonify(
                {"success": False, "error": "명령어나 오디오 파일이 변형되었습니다."}
            ),
            400,
        )

    audio = request.files["audio"]
    instruction = request.form["instruction"]

    # Convert instruction to safe ASCII for folder name
    safe_instruction = unidecode(instruction)

    # Create directory for this instruction if it doesn't exist
    instruction_folder = os.path.join(UPLOAD_FOLDER, safe_instruction)
    os.makedirs(instruction_folder, exist_ok=True)

    # Create a secure filename for saving
    filename = secure_filename(f"{safe_instruction}_{audio.filename}")
    save_path = os.path.join(instruction_folder, filename)

    # Save the audio file to the instruction folder
    audio.save(save_path)

    return jsonify({"success": True, "filename": filename})
