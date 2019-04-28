"""
Actions to perform for characters

"""
from random import randint

import actions_api.combat_effects as combat_effects
from character.models import PlayerClasses, Abilities


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


def do_combat_round(player, target, player_attack_type, enhanced=False):
    """
    Function to complete one round of combat

    :param player: Class of player
    :param target: Class of target
    :param player_attack_type: Rock/paper/scissors/lizard/spock
    :param enhanced: Boolean to tell if to enhance an attack

    :return: dict(player_hp, target_hp)

    """
    player_class = PlayerClasses.objects.get(player_class=player.character_class)
    target_class = PlayerClasses.objects.get(player_class=target.character_class)

    #target_attack = randint(0, 4)
    target_attack = 2
    target_attack_type = number_to_name(target_attack)
    player_attack = name_to_number(player_attack_type)

    # Player wins!
    if (target_attack + 1) % 5 == player_attack:
        ability = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability, player, target)
        print(f"Player wins! (first if) Using {ability} on {target}")

    # Player wins!
    elif (target_attack + 2) % 5 == player_attack:
        ability = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability, player, target)
        print(f"Player wins! (second if) Using {ability} on {target}")

    # Player and computer tie (clash)
    elif target_attack == player_attack:
        # Player's attack
        ability1 = Abilities.objects.get(class_id=player_class, type=player_attack_type)
        collect_and_resolve_effects(ability1, player, target)

        # Target's attack
        ability2 = Abilities.objects.get(class_id=target_class, type=target_attack_type)
        collect_and_resolve_effects(ability2, player, target)
        print(f"Player and target tie! Using both {ability1} on {target} and {ability2} on {player}")

    # Target wins!
    else:
        ability = Abilities.objects.get(class_id=target_class, type=player_attack_type)
        print(f"Target wins! Using {ability} on {player}")

        # Call effect functions
        collect_and_resolve_effects(ability, target, player)

    print(f"Player HP after combat round: {player.hit_points}")
    print(f"Target HP after combat round: {target.hit_points}")
    return player, target


def collect_and_resolve_effects(ability, player, target):
    """
    Function to go through the effects tied to a given ability
    and resolve the cumulative effect of all of them

    :param ability: Queryset for the ability being evaluated, of the form:
                    Abilities.objects.get(class_id=target_class, type=player_attack_type)
    :param player: The player using the ability
    :param target: The target/enemy

    :return: Cumulative effect and an update/save call to the database

    """
    translation_dictionary = {'target': target, 'player': player}

    # Call effect functions
    for effect in ability.ability_effects.values():
        print(effect)
        player, target = getattr(combat_effects, effect['function'])(value=effect['value'],
                                                                     player=player,
                                                                     target=translation_dictionary[effect['target']])
    return player, target
