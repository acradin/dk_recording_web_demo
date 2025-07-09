from models.instruction import Instruction
from extensions import db
from unidecode import unidecode


def get_instruction_list():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Get a list of all instruction dicts (for recording page).

    Args:
        None
    Returns:
        List of instruction dicts (list of dict)
    """
    # Query all instructions and return as dicts with label and folder
    return [
        {"label": i.text, "folder": unidecode(i.text)}
        for i in Instruction.query.order_by(Instruction.created_at).all()
    ]


def get_all_instructions():
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Get all instruction objects (for admin page).

    Args:
        None
    Returns:
        List of Instruction objects
    """
    # Query all instruction objects
    return Instruction.query.order_by(Instruction.created_at).all()


def add_instruction(text):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Add a new instruction to the database.

    Args:
        text: The instruction text to add (str)
    Returns:
        The created Instruction object
    """
    # Create and add a new instruction
    instruction = Instruction(text=text)
    db.session.add(instruction)
    db.session.commit()
    return instruction


def update_instruction(instruction_id, new_text):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Update the text of an existing instruction.

    Args:
        instruction_id: ID of the instruction to update (int)
        new_text: New text for the instruction (str)
    Returns:
        The updated Instruction object, or None if not found
    """
    # Find and update the instruction
    instruction = Instruction.query.get(instruction_id)
    if instruction:
        instruction.text = new_text
        db.session.commit()
    return instruction


def delete_instruction(instruction_id):
    """
    Date: 2025-06-29
    Author: Minjun Park
    Description: Delete an instruction from the database.

    Args:
        instruction_id: ID of the instruction to delete (int)
    Returns:
        The deleted Instruction object, or None if not found
    """
    # Find and delete the instruction
    instruction = Instruction.query.get(instruction_id)
    if instruction:
        db.session.delete(instruction)
        db.session.commit()
    return instruction
