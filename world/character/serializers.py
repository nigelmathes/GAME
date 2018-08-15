from rest_framework import serializers
from commands_api.models import Commands


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commands
        fields = '__all__'
