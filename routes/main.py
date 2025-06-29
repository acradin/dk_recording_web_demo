from flask import Blueprint, render_template
from services.demo_service import get_demo_message

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    message = get_demo_message()
    return render_template("index.html", message=message)
