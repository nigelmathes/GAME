from commands_api.models import Commands
from commands_api.serializers import CommandSerializer
from rest_framework import generics


class CommandsListCreate(generics.ListCreateAPIView):
    queryset = Commands.objects.all()
    serializer_class = CommandSerializer
