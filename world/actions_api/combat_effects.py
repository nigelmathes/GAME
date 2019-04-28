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


def healing(value, player, target):
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
