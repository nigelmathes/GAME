from django.db import models
from django.contrib.gis.db import models as geo_models


class Character(models.Model):
    owner = models.ForeignKey('auth.User', related_name='characters', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    character_class = models.CharField(max_length=20)
    location = geo_models.PointField(
        null=True, blank=False, srid=4326, verbose_name="Location")
    in_combat = models.BooleanField()
    hit_points = models.FloatField()
    appearance = models.TextField()


class Abilities(models.Model):
    ability_name = models.CharField(max_length=20)
    character_class = models.CharField(max_length=20)
    ability_type = models.CharField(max_length=10)  # Attack/Area/Dodge/Block/Disrupt
    added_effect = models.CharField(max_length=20)
    damage = models.IntegerField()
    heal = models.IntegerField()
    message = models.TextField()
