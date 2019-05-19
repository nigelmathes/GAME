from character.models import StatusEffects


def damage(value, target):
    """
    Deal damage

    :param value: How much damage to do to target
    :param target: The character being damaged

    :return: Updated target

    """
    target.hit_points -= value

    return target


def heal(value, target):
    """
    Do healing

    :param value: How much damage to do to target
    :param target: The character being healed

    :return: Updated target

    """
    target.hit_points += value

    return target


def prone(value, target):
    """
    Make the target prone:
    Next turn, target’s block does not beat area
    
    :param value: How long the effect lasts
    :param target: The character being affected by prone

    :return: Updated target

    """
    status_entry = StatusEffects(character_id=target, name='prone', duration=value)

    # Add the prone status effect to the StatusEffects database
    status_entry.save()

    return target
