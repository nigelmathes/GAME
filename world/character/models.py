from django.db import models


class Character(models.Model):
    """
    Table to hold information about a player's character
    """
    owner = models.ForeignKey('auth.User', related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    character_class = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=7, default=0.0000000)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, default=0.0000000)
    in_combat = models.BooleanField(default=False)
    target = models.CharField(max_length=50, default="None")
    hit_points = models.IntegerField(default=500)
    ex_meter = models.IntegerField(default=1000)
    appearance = models.TextField(default="No entry - you must be hella ugly")


class PlayerClasses(models.Model):
    """
    Table to hold the list of playable classes
    """
    player_class = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.player_class}"


class Abilities(models.Model):
    """
    Table to hold the list of abilities
    """
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)  # Attack/Area/Dodge/Block/Disrupt
    description = models.CharField(max_length=80)
    class_id = models.ForeignKey(PlayerClasses, related_name='class_abilities', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.class_id.player_class} - {self.name}"


class AbilityEffects(models.Model):
    """
    Table to hold the list of base ability effects, which are things like:
        damage
        healing

    General rule: Effects take place immediately and serve as base skills if you don't enhance the skill
    """
    # Ability ID points back to the Abilities table
    ability_id = models.ForeignKey(Abilities, related_name='ability_effects', on_delete=models.DO_NOTHING)
    function = models.CharField(max_length=20)
    value = models.IntegerField()
    target = models.CharField(max_length=10, default='target')

    def __str__(self):
        return f"{self.ability_id.name} - {self.function} {self.target}"


class AbilityEnhancements(models.Model):
    """
    Table to hold the list of ability enhancements, which are things like:
        advantage
        extra healing
        extra damage
        swap weapon

    General rule: Enhancements are added class abilities and can take place over multiple rounds

    value corresponds to the numeric effect of the enhancement, e.g.
        For name = 'slow', function = 'duration', and value = 1, representing 1 round of slow
    """
    # Ability ID points back to the Abilities table
    ability_id = models.ForeignKey(Abilities, related_name='ability_enhancements', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)
    function = models.CharField(max_length=20)
    value = models.IntegerField()
    target = models.CharField(max_length=10, default='target')

    def __str__(self):
        return f"{self.ability_id.name} - {self.name}, {self.function}"


class StatusEffects(models.Model):
    """
    Table to hold list of status effects as a foreign key relationship to the Character model
    """
    # Character ID points back to the Character table
    character_id = models.ForeignKey(Character, related_name='status_effects', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.character_id.name} - {self.name}"
