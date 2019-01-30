"""
Actions to perform for characters

"""
from character.models import Character


def level_up():
    """
    Gets the player character and then updates the level.

    """
    queryset = Character.objects.all()


def create_character():
    """
    Creates a character

    """
    pass
