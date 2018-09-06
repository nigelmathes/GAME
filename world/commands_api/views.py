from commands_api.models import Commands
from commands_api.serializers import CommandSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import spacy
import en_core_web_md

#nlp = en_core_web_md.load()


class CommandsListCreate(generics.ListCreateAPIView):
    queryset = Commands.objects.all()
    serializer_class = CommandSerializer


class MatchCommands(APIView):
    """
    Match GET request input to Commands database and return result

    """

    def get(self, request):

        input_command = request.query_params.get('input_data', None)
        context = request.query_params.get('context')

        # Catch null context in request
        if not context:
            context = ''

        #message_token = nlp(input_command)

        commands = Commands.objects.filter(context=context)
        commands_strings = commands.values_list('command', flat=True)

        command_list = []
        similarity_list = []
        for command in commands_strings:

            command_list.append(command)
            command_token = nlp(command)
            similarity = message_token.similarity(command_token)
            similarity_list.append(similarity)

        if similarity_list:
            matching_index = similarity_list.index(max(similarity_list))
            matching_command = commands[matching_index]
        else:
            matching_command = Commands.objects.get(pk=1)

        serializer = CommandSerializer(matching_command)
        return Response(serializer.data)

    def post(self):
        print(self.request.POST.get('test_val'))
        return Response("I think it worked")
