from flask import Blueprint, render_template, request, jsonify, send_from_directory
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


@instruction_bp.route("/audio-files-by-label", methods=["POST"])
def audio_files_by_label():
    """
    Date: 2025-07-09
    Author: Minjun Park
    Description: 주어진 명령어(label)에 해당하는 오디오 파일 목록을 반환합니다.
    Args:
        label: 명령어 라벨 (POST JSON)
    Returns:
        JSON (files: 오디오 파일명 리스트, folder: 폴더명)
    """
    label = request.json.get("label")
    if not label:
        return jsonify({"files": []})
    folder = unidecode(label)
    upload_dir = os.path.join("uploads", folder)
    if not os.path.isdir(upload_dir):
        return jsonify({"files": []})
    files = [f for f in os.listdir(upload_dir) if f.endswith(".wav")]
    return jsonify({"files": files, "folder": folder})


@instruction_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """
    Date: 2025-07-09
    Author: Minjun Park
    Description: 업로드된 오디오 파일을 클라이언트에 서빙합니다.
    Args:
        filename: 요청된 파일 경로 (URL param)
    Returns:
        오디오 파일 (send_from_directory)
    """
    return send_from_directory("uploads", filename)
