from character.models import StatusEffects


def inflict_damage(value, target):
    """
    Deal damage

    :param value: How much damage to do to target
    :param target: The character being damaged

    :return: Updated target
    """
    target.hit_points -= value

    return target


def inflict_heal(value, target):
    """
    Do healing

    :param value: How much damage to do to target
    :param target: The character being healed

    :return: Updated target
    """
    target.hit_points += value

    return target


def inflict_prone(value, target):
    """
    Make the target prone by adding the status effect to the target's statuses
    Next turn, target’s block does not beat area
    
    :param value: How long the effect lasts
    :param target: The character receiving the 'prone' status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='prone', duration=value)

    # Add the prone status effect to the StatusEffects database
    status_entry.save()

    return target


def apply_prone(target, rules, left):
    """
    Apply the effects of prone to the target:
    Next turn, target’s block does not beat area. Will transform:

        "block": {"beats": ["attack", "area"], "loses": ["disrupt", "dodge"]}
        "area": {"beats": ["disrupt", "dodge"], "loses": ["attack", "block"]},

                                    to...(left==True)

        "block": {"beats": ["attack"], "loses": ["disrupt", "dodge", "area"]}

                                    or...(left==False)

        "area": {"beats": ["disrupt", "dodge", "block"], "loses": ["attack"]}

    :param target: The character being affected by prone
    :param rules: The ruleset to edit
    :param left: Position of the target (left or right, corresponding to left/right keys in rules dict)

    :return: Updated target and ruleset
    """
    # If left, then the target is the primary and the left keys for the rules should be edited
    if left:
        # Remove area from the block: beats dict
        if "area" in rules["block"]["beats"]:
            rules["block"]["beats"].remove("area")

        # Add area to the block: loses dict
        if "area" not in rules["block"]["loses"]:
            rules["block"]["loses"].append("area")
    # If right (not left), then the target is the secondary and the right keys for the rules should be edited
    else:
        # Remove block from the area: loses dict
        if "block" in rules["area"]["loses"]:
            rules["area"]["loses"].remove("block")

        # Add block to the area: beats dict
        if "block" not in rules["area"]["beats"]:
            rules["area"]["beats"].append("block")

    return target, rules
