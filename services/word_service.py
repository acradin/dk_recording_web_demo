from models.word import Word
from extensions import db


def get_word_list():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Get a list of all word texts (for recording page).

    Args:
        None
    Returns:
        List of word texts (list of str)
    """
    # Query all words and return their text
    return [w.text for w in Word.query.order_by(Word.created_at).all()]


def get_all_words():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Get all word objects (for admin page).

    Args:
        None
    Returns:
        List of Word objects
    """
    # Query all word objects
    return Word.query.order_by(Word.created_at).all()


def add_word(text):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Add a new word to the database.

    Args:
        text: The word text to add (str)
    Returns:
        The created Word object
    """
    # Create and add a new word
    word = Word(text=text)
    db.session.add(word)
    db.session.commit()
    return word


def update_word(word_id, new_text):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Update the text of an existing word.

    Args:
        word_id: ID of the word to update (int)
        new_text: New text for the word (str)
    Returns:
        The updated Word object, or None if not found
    """
    # Find and update the word
    word = Word.query.get(word_id)
    if word:
        word.text = new_text
        db.session.commit()
    return word


def delete_word(word_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Delete a word from the database.

    Args:
        word_id: ID of the word to delete (int)
    Returns:
        The deleted Word object, or None if not found
    """
    # Find and delete the word
    word = Word.query.get(word_id)
    if word:
        db.session.delete(word)
        db.session.commit()
    return word
