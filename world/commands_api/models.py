from django.db import models
from django.contrib.gis.db import models as geo_models


class Commands(models.Model):
    """
    Command is the string you're trying to match
    Action is the action for the code to take (function to call)
    Message is what is returned to the user, which will be transformed from text to speedh
    """
    command = models.CharField(max_length=300)
    action = models.CharField(max_length=300)
    message = models.TextField()
