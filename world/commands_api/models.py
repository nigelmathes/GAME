from django.db import models


class Commands(models.Model):
    command = models.CharField(max_length=300)
    action = models.CharField(max_length=300)
    message = models.TextField()
