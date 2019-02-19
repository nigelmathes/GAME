from django.db import models
from django.contrib.gis.db import models as geo_models


class Character(models.Model):
    """
    Table to hold information about a player's character
    """
    owner = models.ForeignKey('auth.User', related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    character_class = models.CharField(max_length=20)
    location = geo_models.PointField(
        null=True, blank=False, srid=4326, verbose_name="Location")
    in_combat = models.BooleanField()
    target = models.CharField(max_length=50)
    hit_points = models.IntegerField()
    ex_meter = models.IntegerField()
    appearance = models.TextField()


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
    ability_name = models.CharField(max_length=20)
    ability_type = models.CharField(max_length=20)  # Attack/Area/Dodge/Block/Disrupt
    ability_description = models.CharField(max_length=80)
    class_id = models.ForeignKey(PlayerClasses, related_name='class_abilities', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.ability_name}"


class AbilityEffects(models.Model):
    """
    Table to hold the list of base ability effects, which are things like:
        damage
        healing

    General rule: Effects take place immediately and serve as base skills if you don't enhance the skill
    """
    # Ability ID points back to the Abilities table
    ability_id = models.ForeignKey(Abilities, related_name='ability_effects', on_delete=models.DO_NOTHING)
    effect_name = models.CharField(max_length=20)
    point_value = models.IntegerField()


class AbilityEnhancements(models.Model):
    """
    Table to hold the list of ability enhancements, which are things like:
        advantage
        extra healing
        extra damage
        swap weapon

    General rule: Enhancements are added class abilities and can take place over multiple rounds

    point_value corresponds to the numeric effect of the enhancement, e.g.
        For 'slow', enhancement_type = 'duration', and point_value = 1, representing 1 round of slow
    """
    # Ability ID points back to the Abilities table
    ability_id = models.ForeignKey(Abilities, related_name='ability_enhancements', on_delete=models.DO_NOTHING)
    enhancement_name = models.CharField(max_length=20)
    enhancement_type = models.CharField(max_length=20)
    point_value = models.IntegerField()

    def __str__(self):
        return f"{self.enhancement_name}"
