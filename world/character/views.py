from rest_framework import generics

from character.models import Character, Abilities
from character.serializers import CharacterSerializer, AbilitySerializer


class CharacterList(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class AbilityList(generics.ListAPIView):
    queryset = Abilities.objects.all()
    serializer_class = AbilitySerializer


class CreateCharacter():
    """ Class to create a character """

    def put(self, request, format=None):
        pass


class UpdateCharacter():
    pass
