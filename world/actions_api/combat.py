"""
Actions to perform for characters

"""
from random import randint

import actions_api.combat_effects as combat_effects
from character.models import PlayerClasses, Abilities, AbilityEffects


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


def do_combat_round(player, target, attack_type, enhanced=False):
    """
    Function to complete one round of combat

    :param player: Class of player
    :param target: Class of target
    :param attack_type: Rock/paper/scissors/lizard/spock
    :param enhanced: Boolean to tell if to enhance an attack

    :return: dict(player_hp, target_hp)

    """
    player_class = PlayerClasses.objects.get(player_class=player.character_class)
    target_class = PlayerClasses.objects.get(player_class=target.character_class)

    #target_attack = randint(0, 4)
    target_attack = 2
    player_attack = name_to_number(attack_type)
    player_ability = Abilities.objects.get(class_id=player_class, type=attack_type)

    if (target_attack + 1) % 5 == player_attack:
        # Player wins
        # Get player's attack details
        ability = PlayerClasses.objects.get(class_abilities=attack_type)
        effects = ability.effects
        pass

    elif (target_attack + 2) % 5 == player_attack:
        # Player wins!
        ability = PlayerClasses.objects.get(class_abilities=attack_type)
        pass

    elif target_attack == player_attack:
        # Player and computer tie (clash)
        ability = PlayerClasses.objects.get(class_abilities=attack_type)
        pass

    else:
        # Target wins
        #ability = PlayerClasses.objects.get(class_abilities=attack_type)
        print(player_class)
        print(player_class.class_abilities.values())
        print(player_ability)
        print(player_ability.ability_effects.values())
        print(player_class.class_abilities.values())

        # Call effect functions
        for effect in player_ability.ability_effects.values():
            result = getattr(combat_effects, effect['function'])(value=effect['value'], target=target.id)

    # Determine results, update tables

    return []
