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


def inflict_percent_damage(value, target):
    """
    Deal percent health damage

    :param value: How much % of current HP damage to do to target
    :param target: The character being damaged

    :return: Updated target
    """
    target.hit_points -= (value / 100.) * target.hit_points
    print(f"Inflicted {(value / 100.) * target.hit_points} damage via poison!")

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
def apply_prone(target, rules, added_effects, left):
    """
    Apply the effects of prone to the target:
    Next turn, target’s block does not beat area.

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param added_effects: Additional ability effects
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

    return target, rules, added_effects


# Enhanced effect of Dreamer's Fold Earth - disorient
def inflict_disorient(value, target):
    """
    Make the target disoriented by adding the status effect to the target's statuses

    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='disorient', duration=value)

    # Add the disorient status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of Dreamer's Fold Earth - disorient
def apply_disorient(target, rules, added_effects, left):
    """
    Apply the effects of disorient to the target:
    Next turn, target’s dodge does not beat attack.

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param added_effects: Additional ability effects
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

    # "attack": {"beats": ["area", "disrupt", "dodge"], "loses": ["block"]}
    else:
        # Remove block from the area: loses dict
        if "dodge" in rules["attack"]["loses"]:
            rules["attack"]["loses"].remove("dodge")

        # Add block to the area: beats dict
        if "dodge" not in rules["attack"]["beats"]:
            rules["attack"]["beats"].append("dodge")

    return target, rules, added_effects


# Enhanced effect of Chosen's Extreme Speed - haste
def inflict_haste(value, target):
    """
    Make the target hasted by adding the status effect to the target's statuses

    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='haste', duration=value)

    # Add the haste status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of Chosen's Extreme Speed - haste
def apply_haste(target, rules, added_effects, left):
    """
    Apply the effects of haste to the target:
    Next turn, target's attack will beat an opposing attack (no clash)

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param added_effects: Additional ability effects
    :param left: Position of the target (left or right, corresponding to left/right keys in rules dict)

    :return: Updated target and ruleset
    """
    # "attack": {"beats": ["disrupt", "area", "attack"], "loses": ["block", "dodge"]}
    if left:
        # Remove attack from the attack: loses dict
        if "attack" in rules["attack"]["loses"]:
            rules["attack"]["loses"].remove("attack")

        # Add attack to the attack: beats dict
        if "attack" not in rules["attack"]["beats"]:
            rules["attack"]["beats"].append("attack")

    # "attack": {"beats": ["disrupt", "area"], "loses": ["block", "dodge", "attack"]}
    else:
        # Remove attack from the attack: beats dict
        if "attack" in rules["attack"]["beats"]:
            rules["attack"]["beats"].remove("attack")

        # Add attack to the attack: loses dict
        if "attack" not in rules["attack"]["loses"]:
            rules["attack"]["loses"].append("attack")

    return target, rules, added_effects


# Enhanced effect of NOT IMPLEMENTED
def inflict_delayed_double_damage(value, target):
    """
    Make the target's next attack do double damage by
    adding the status effect to the target's statuses

    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='double_damage', duration=value)

    # Add the double damage status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of NOT IMPLEMENTED
def apply_delayed_double_damage(target, rules, added_effects, left):
    """
    Apply the effects of double_damage to the target:
    Next turn, target's attack will do double damage

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param added_effects: Additional ability effects
    :param left: Position of the target (left or right, corresponding to left/right keys in rules dict)

    :return: Updated target, ruleset, and/or added_effects
    """
    added_effects.append({'function': 'damage', 'value': 100, 'target': 'target'})

    return target, rules, added_effects


# Enhanced effect of Chemist's Poison Dart
def inflict_poison(value, target):
    """
    Make the target take damage for value rounds by
    adding the status effect to the target's statuses

    :param value: How long the effect lasts
    :param target: The character receiving the status effect

    :return: Updated target
    """
    status_entry = StatusEffects(character_id=target, name='poison', duration=value)

    # Add the poison status effect to the StatusEffects database
    status_entry.save()

    return target


# Enhanced effect of Chemist's Poison Dart
def apply_poison(target, rules, added_effects, left):
    """
    Apply the effects of poison to the target:
    Take 10% HP damage

    :param target: The character being affected
    :param rules: The ruleset to edit
    :param added_effects: Additional ability effects
    :param left: Position of the target (left or right,
                 corresponding to left/right keys in rules dict)

    :return: Updated target, ruleset, and/or added_effects
    """
    if left:
        added_effects.append({'function': 'percent_damage', 'value': 10, 'target': 'self'})
    else:
        added_effects.append({'function': 'percent_damage', 'value': 10, 'target': 'target'})

    return target, rules, added_effects

