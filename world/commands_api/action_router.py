"""
Takes input commands and routes to a function which completes the action.

Imports from the subapp/character_actions.py file, and then calls functions within those files.

"""

from character import character_actions


def create_character():
    """
    Create a character from the character subapp.

    """
    character_actions.create_character()

