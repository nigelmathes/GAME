def damage(value, target):
    """
    Deal damage.

    :param value: How much damage to do to target
    :param target: The character being damaged

    :return:

    """
    print(f"DOING {value} DAMAGE TO {target}")
    print(f"TARGET INITIAL HIT POINTS: {target.hit_points}")
    target.hit_points -= value
    print(f"TARGET FINAL HIT POINTS: {target.hit_points}")

    pass
