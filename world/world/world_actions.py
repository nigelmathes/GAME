"""
Actions to perform while out in the world

"""
from character.models import Character


def get_item(character_id, item_name):
    """
    Gets an item and puts it in the player's inventory

    """
    player_character = Character.objects.get(character_id)



def create_character():
    """
    Creates a character

    """
    pass
