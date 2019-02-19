from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets

from character.models import Character, Abilities, AbilityEffects, AbilityEnhancements, PlayerClasses
from character.serializers import CharacterSerializer, AbilitySerializer, UserSerializer,\
    AbilityEffectsSerializer, PlayerClassesSerializer, AbilityEnhancementsSerializer
from character.permissions import IsOwnerOrReadOnly


class CharacterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AbilityViewSet(viewsets.ModelViewSet):
    queryset = Abilities.objects.all()
    serializer_class = AbilitySerializer


class AbilityEffectViewSet(viewsets.ModelViewSet):
    queryset = AbilityEffects.objects.all()
    serializer_class = AbilityEffectsSerializer


class AbilityEnhancementsViewSet(viewsets.ModelViewSet):
    queryset = AbilityEnhancements.objects.all()
    serializer_class = AbilityEnhancementsSerializer


class PlayerClassesViewSet(viewsets.ModelViewSet):
    queryset = PlayerClasses.objects.all()
    serializer_class = PlayerClassesSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
