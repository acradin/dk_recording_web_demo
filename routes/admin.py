from flask import Blueprint, render_template, request, redirect, url_for
from services.word_service import get_all_words, add_word, update_word, delete_word

# Create a Blueprint for admin-related routes
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/words", methods=["GET", "POST"])
def admin_words():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Admin page for managing words (list, add).

    Args:
        text: New word to add (POST, form field)
    Returns:
        Rendered admin_words.html template with word list.
    """
    # Handle new word addition
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            add_word(text)
        return redirect(url_for("admin.admin_words"))
    # Get all words for display
    words = get_all_words()
    return render_template("admin_words.html", words=words)


@admin_bp.route("/words/edit/<int:word_id>", methods=["POST"])
def edit_word(word_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Edit an existing word.

    Args:
        word_id: ID of the word to edit (URL param)
        text: New word text (POST, form field)
    Returns:
        Redirects to admin_words page.
    """
    # Update the word with new text
    new_text = request.form.get("text")
    if new_text:
        update_word(word_id, new_text)
    return redirect(url_for("admin.admin_words"))


@admin_bp.route("/words/delete/<int:word_id>", methods=["POST"])
def delete_word_route(word_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Delete a word from the database.

    Args:
        word_id: ID of the word to delete (URL param)
    Returns:
        Redirects to admin_words page.
    """
    # Delete the word from the database
    delete_word(word_id)
    return redirect(url_for("admin.admin_words"))
