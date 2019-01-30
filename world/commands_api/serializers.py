from rest_framework import serializers
from commands_api.models import Commands


class CommandSerializer(serializers.ModelSerializer):
    """
    Return only the message to the user.
    """
    class Meta:
        model = Commands
        fields = ['message']
