from rest_framework import generics

from character.models import Character
from character.serializers import CharacterSerializer


class CharacterList(generics.ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class CreateCharacter():
    """ Class to create a character """

    def put(self, request, format=None):
        pass


class UpdateCharacter():
    pass
