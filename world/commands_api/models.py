from django.db import models


class Commands(models.Model):
    """
    Command is the string you're trying to match
    Action is the action for the code to take (function to call)
    Message is what is returned to the user, which will be transformed from text to speedh
    """
    command = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    message = models.TextField()
    context = models.CharField(max_length=100)
