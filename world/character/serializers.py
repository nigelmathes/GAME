from rest_framework import serializers
from character.models import Character, Abilities


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Abilities
        fields = '__all__'
