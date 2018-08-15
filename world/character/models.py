from django.db import models
from django.contrib.gis.db import models as geo_models


class Character(models.Model):
    name = models.CharField(max_length=300)
    account = models.CharField(max_length=300)
    character_class = models.TextField()
    level = models.FloatField()
    location = geo_models.PointField(
        null=True, blank=False, srid=4326, verbose_name="Location")
    in_combat = models.BooleanField()
    hit_points = models.FloatField()
