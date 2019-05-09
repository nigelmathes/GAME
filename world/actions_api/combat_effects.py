from character.models import StatusEffects

def damage(value, player, target):
    """
    Deal damage.

    :param value: How much damage to do to target
    :param player: The character doing the damaging
    :param target: The character being damaged

    :return: Updated player, target

    """
    print(f"DOING {value} DAMAGE TO {target}")
    target.hit_points -= value

    return player, target


def heal(value, player, target):
    """
    Do healing

    :param value: How much damage to do to target
    :param player: The character doing the healing
    :param target: The character being healed

    :return: Updated player, target

    """
    print(f"DOING {value} HEALING TO {target}")
    target.hit_points += value

    return player, target


def prone(value, player, target):
    """
    Make the target prone:
    Next turn, opponent’s block does not beat area
    
    :param value: How long the effect lasts
    :param player: The character using prone
    :param target: The character being affected by prone

    :return: Updated player, target

    """
    print(f"{target} will be prone for {value} rounds")
    status_entry = StatusEffects(character_id=player, name='prone', duration=1)
    status_entry.save()

    return player, target
