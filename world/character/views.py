from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets

from character.models import Character, Abilities
from character.serializers import CharacterSerializer, AbilitySerializer, UserSerializer
from character.permissions import IsOwnerOrReadOnly


class CharacterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AbilityList(generics.ListAPIView):
    queryset = Abilities.objects.all()
    serializer_class = AbilitySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateCharacter():
    """ Class to create a character """

    def put(self, request, format=None):
        pass


class UpdateCharacter():
    pass
