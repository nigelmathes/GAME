from django.db import models
from django.contrib.gis.db import models as geo_models


class Commands(models.Model):
    command = models.CharField(max_length=300)
    action = models.CharField(max_length=300)
    message = models.TextField()
    location = geo_models.PointField(
        null=True, blank=False, srid=4326, verbose_name="Location")
