"""
Actions to perform for characters

"""
from random import randint

from character.models import Character


def number_to_name(num):
    """
    Convert integer number to move name

    :param num: Integer corresponding to move

    :return: String name of move

    """
    if num == 0:
        result = "area"
    elif num == 1:
        result = "attack"
    elif num == 2:
        result = "block"
    elif num == 3:
        result = "disrupt"
    elif num == 4:
        result = "dodge"
    else:
        result = "attack"

    return result


def name_to_number(name):
    """
    Convert move name to integer number

    :param name: String name of move

    :return: Integer corresponding to move

    """
    if name == "area":
        result = 0
    elif name == "attack":
        result = 1
    elif name == "block":
        result = 2
    elif name == "disrupt":
        result = 3
    elif name == "dodge":
        result = 4
    else:
        result = 1

    return result


def do_combat_round(type, target):
    """
    Function to complete one round of combat

    :param type:
    :param target:

    :return: dict(player_hp, target_hp)

    """
    target_attack = randint(0, 4)

    player_attack = name_to_number(type)

    if (target_attack + 1) % 5 == player_attack:
        # Player wins
        # Get player's attack details
        pass

    elif (target_attack + 2) % 5 == player_attack:
        # Player wins!
        pass

    elif target_attack == player_attack:
        # Player and computer tie (clash)
        pass

    else:
        # Target wins
        pass

    # Determine results
    return []


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
