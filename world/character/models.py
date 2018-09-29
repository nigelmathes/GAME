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
    hit_points = models.FloatField()
    appearance = models.TextField()


class PlayerClasses(models.Model):
    """
    Table to hold the list of playable classes
    """
    player_class = models.CharField(max_length=20)


class Abilities(models.Model):
    """
    Table to hold the list of abilities
    """
    ability_name = models.CharField(max_length=20)
    ability_type = models.CharField(max_length=10)  # Attack/Area/Dodge/Block/Disrupt


class AbilityEffects(models.Model):
    """
    Table to hold the list of ability effects
    """
    ability_id = models.ForeignKey(Abilities, related_name='ability_effects', on_delete=models.DO_NOTHING)
    effect = models.CharField(max_length=20)
    damage = models.IntegerField()
    heal = models.IntegerField()


class AbilityMessages(models.Model):
    """
    Table to hold ability descriptions/messages to select from
    """
    ability_id = models.ForeignKey(Abilities, related_name='ability_messages', on_delete=models.DO_NOTHING)
    message = models.TextField()
