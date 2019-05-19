"""
Actions to perform for characters

"""
from random import randint

import actions_api.combat_effects as combat_effects
from character.models import PlayerClasses, Abilities, StatusEffects


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
        result = "dodge"
    elif num == 4:
        result = "disrupt"
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
    elif name == "dodge":
        result = 3
    elif name == "disrupt":
        result = 4
    else:
        result = 1

    return result


def do_combat_round(player, target, player_attack_type, enhanced=False):
    """
    Function to complete one round of combat

    :param player: Class of player
    :param target: Class of target
    :param player_attack_type: area/attack/block/dodge/disrupt
    :param enhanced: Boolean to tell if to enhance an attack

    :return: Updated player, target objects

    Area (0) beats Disrupt (3) and Dodge (4)
    Attack (1) beats Disrupt (3) and Area (0)
    Block (2) beats Attack (1) and Area (0)
    Disrupt (3) beats Block (2) and Dodge (4)
    Dodge (4) beats Attack (1) and Block (2)

    """
    player_class = PlayerClasses.objects.get(player_class=player.character_class)
    target_class = PlayerClasses.objects.get(player_class=target.character_class)

    target_attack = randint(0, 4)
    target_attack_type = number_to_name(target_attack)
    player_attack = name_to_number(player_attack_type)

    #check_and_apply_status(player)
    #check_and_apply_status(target)

    print(f"Player uses {player_attack_type} ({player_attack}), target uses {target_attack_type} ({target_attack})")
    # Player wins!
    if (target_attack + 1) % 5 == player_attack:
        ability = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability, winner=player, loser=target, enhanced=enhanced)
        print(f"Player wins! (first if) Using {ability} ({player_attack} on {target}")

    # Player wins!
    elif (target_attack + 2) % 5 == player_attack:
        ability = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability, winner=player, loser=target, enhanced=enhanced)
        print(f"Player wins! (second if) Using {ability} on {target}")

    # Player and computer tie (clash)
    elif target_attack == player_attack:
        # Player's attack
        ability1 = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability1, winner=player, loser=target, enhanced=enhanced)

        # Target's attack
        ability2 = Abilities.objects.get(class_id=target_class, type=target_attack_type)
        collect_and_resolve_effects(ability2, winner=target, loser=player, enhanced=enhanced)
        print(f"Player and target tie! Using both {ability1} on {target} and {ability2} on {player}")

    # Target wins!
    else:
        ability = Abilities.objects.get(class_id=target_class, type=target_attack_type)
        print(f"Target wins! Using {ability} on {player}")

        # Call effect functions
        collect_and_resolve_effects(ability, winner=target, loser=player, enhanced=enhanced)

    print(f"Player HP after combat round: {player.hit_points}")
    print(f"Target HP after combat round: {target.hit_points}\n")
    return player, target


def check_and_apply_status(character):
    """
    Function to check player and target status effects, and apply those effects before combat

    :param character: A character object to check status for

    :return: Updated rules for combat based upon effects

    """
    statuses = character.status_effects

    for status in statuses:
        pass


def collect_and_resolve_effects(ability, winner, loser, enhanced=False):
    """
    Function to go through the effects tied to a given ability
    and resolve the cumulative effect of all of them

    :param ability: Queryset for the ability being evaluated, of the form:
                    Abilities.objects.get(class_id=target_class, type=player_attack_type)
    :param winner: The player using the ability
    :param loser: The target/enemy
    :param enhanced: Boolean to tell if to enhance an attack

    :return: Cumulative effect and an update/save call to the database

    """
    translation_dictionary = {'target': loser, 'self': winner}

    # Call effect functions
    for effect in ability.ability_effects.values():
        translation_dictionary[effect['target']] = \
            getattr(combat_effects, effect['function'])(value=effect['value'],
                                                        target=translation_dictionary[effect['target']])

    # Add enhancement if it exists
    if enhanced:
        for enhancement in ability.ability_enhancements.values():
            translation_dictionary[enhancement['target']] = \
                getattr(combat_effects, enhancement['function'])(value=enhancement['value'],
                                                                 target=translation_dictionary[enhancement['target']])
    return winner, loser
