from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.instruction_service import (
    get_all_instructions,
    add_instruction,
    update_instruction,
    delete_instruction,
)
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

# Create a Blueprint for admin-related routes
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_PASSWORD = os.getenv("SECRET_KEY")


# Decorator for admin authentication check
def admin_login_required(f):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Redirects to login page if admin session is not authenticated.
    Args:
        f: Wrapped function
    Returns:
        Wrapped function with authentication check
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_authenticated"):
            flash("관리자 인증이 필요합니다.")
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Handles admin login (password authentication). Stores session info on success.
    Args:
        password: Admin password (POST form)
    Returns:
        Redirects to admin page on success, renders login form on failure
    """
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_authenticated"] = True
            return redirect(url_for("admin.admin_instructions"))
        else:
            flash("비밀번호가 올바르지 않습니다.")
    return render_template("admin_login.html")


@admin_bp.route("/instructions", methods=["GET", "POST"])
@admin_login_required
def admin_instructions():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Admin page for listing and adding instructions.
    Args:
        text: New instruction to add (POST form)
    Returns:
        Renders admin_instructions.html template with instruction list
    """
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            add_instruction(text)
        return redirect(url_for("admin.admin_instructions"))
    instructions = get_all_instructions()
    return render_template("admin_instructions.html", instructions=instructions)


@admin_bp.route("/instructions/edit/<int:instruction_id>", methods=["POST"])
@admin_login_required
def edit_instruction(instruction_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Edit an existing instruction.
    Args:
        instruction_id: ID of the instruction to edit (URL param)
        text: New instruction text (POST form)
    Returns:
        Redirects to admin_instructions page
    """
    new_text = request.form.get("text")
    if new_text:
        update_instruction(instruction_id, new_text)
    return redirect(url_for("admin.admin_instructions"))


@admin_bp.route("/instructions/delete/<int:instruction_id>", methods=["POST"])
@admin_login_required
def delete_instruction_route(instruction_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Delete an instruction from the database.
    Args:
        instruction_id: ID of the instruction to delete (URL param)
    Returns:
        Redirects to admin_instructions page
    """
    delete_instruction(instruction_id)
    return redirect(url_for("admin.admin_instructions"))
