from flask import Blueprint, render_template, request, redirect, url_for
from services.instruction_service import (
    get_all_instructions,
    add_instruction,
    update_instruction,
    delete_instruction,
)

# Create a Blueprint for admin-related routes
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/instructions", methods=["GET", "POST"])
def admin_instructions():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Admin page for managing instructions (list, add).

    Args:
        text: New instruction to add (POST, form field)
    Returns:
        Rendered admin_instructions.html template with instruction list.
    """
    # Handle new instruction addition
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            add_instruction(text)
        return redirect(url_for("admin.admin_instructions"))
    # Get all instructions for display
    instructions = get_all_instructions()
    return render_template("admin_instructions.html", instructions=instructions)


@admin_bp.route("/instructions/edit/<int:instruction_id>", methods=["POST"])
def edit_instruction(instruction_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Edit an existing instruction.

    Args:
        instruction_id: ID of the instruction to edit (URL param)
        text: New instruction text (POST, form field)
    Returns:
        Redirects to admin_instructions page.
    """
    # Update the instruction with new text
    new_text = request.form.get("text")
    if new_text:
        update_instruction(instruction_id, new_text)
    return redirect(url_for("admin.admin_instructions"))


@admin_bp.route("/instructions/delete/<int:instruction_id>", methods=["POST"])
def delete_instruction_route(instruction_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Delete an instruction from the database.

    Args:
        instruction_id: ID of the instruction to delete (URL param)
    Returns:
        Redirects to admin_instructions page.
    """
    # Delete the instruction from the database
    delete_instruction(instruction_id)
    return redirect(url_for("admin.admin_instructions"))
