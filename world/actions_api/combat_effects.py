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


# Enhanced effect of Dreamer's Moving Sidewalk - prone
def inflict_prone(value, target):
    """
    Make the target prone by adding the status effect to the target's statuses
    Next turn, target’s block does not beat area
    
    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='prone', duration=value)

    # Add the prone status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of Dreamer's Moving Sidewalk - prone
def apply_prone(target, rules, left):
    """
    Apply the effects of prone to the target:
    Next turn, target’s block does not beat area.

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param left: Position of the target (left or right, corresponding to left/right keys in rules dict)

    :return: Updated target and ruleset
    """
    # "block": {"beats": ["attack"], "loses": ["disrupt", "dodge", "area"]}
    if left:
        # Remove area from the block: beats dict
        if "area" in rules["block"]["beats"]:
            rules["block"]["beats"].remove("area")

        # Add area to the block: loses dict
        if "area" not in rules["block"]["loses"]:
            rules["block"]["loses"].append("area")

    # "area": {"beats": ["disrupt", "dodge", "block"], "loses": ["attack"]}
    else:
        # Remove block from the area: loses dict
        if "block" in rules["area"]["loses"]:
            rules["area"]["loses"].remove("block")

        # Add block to the area: beats dict
        if "block" not in rules["area"]["beats"]:
            rules["area"]["beats"].append("block")

    return target, rules


# Enhanced effect of Dreamer's Fold Earth - disorient
def inflict_disorient(value, target):
    """
    Make the target disorient by adding the status effect to the target's statuses

    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='disorient', duration=value)

    # Add the prone status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of Dreamer's Fold Earth - disorient
def apply_disorient(target, rules, left):
    """
    Apply the effects of disorient to the target:
    Next turn, target’s dodge does not beat attack.

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param left: Position of the target (left or right, corresponding to left/right keys in rules dict)

    :return: Updated target and ruleset
    """
    # "dodge": {"beats": ["block"], "loses": ["area", "disrupt", "attack"]}
    if left:
        # Remove area from the block: beats dict
        if "attack" in rules["dodge"]["beats"]:
            rules["dodge"]["beats"].remove("attack")

        # Add area to the block: loses dict
        if "attack" not in rules["dodge"]["loses"]:
            rules["dodge"]["loses"].append("attack")

    # "attack": {"beats": ["area", "disrupt", "attack"], "loses": ["block"]}
    else:
        # Remove block from the area: loses dict
        if "dodge" in rules["attack"]["loses"]:
            rules["attack"]["loses"].remove("dodge")

        # Add block to the area: beats dict
        if "dodge" not in rules["attack"]["beats"]:
            rules["attack"]["beats"].append("dodge")

    return target, rules
