from commands_api.models import Commands
from commands_api.serializers import CommandSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import spacy
import en_core_web_md

nlp = en_core_web_md.load()


class CommandsListCreate(generics.ListCreateAPIView):
    queryset = Commands.objects.all()
    serializer_class = CommandSerializer


class MatchCommands(APIView):
    """
    Match GET request input to Commands database and return result

    """

    @staticmethod
    def get(request):

        input_command = request.query_params.get('input_data', None)
        context = request.query_params.get('context')

        # Catch null context in request
        if not context:
            context = ''

        check_perfect_match = Commands.objects.filter(command=input_command.lower(), context=context)

        # If there is a perfect matching string, return the command
        if check_perfect_match:

            # This is the action to take
            action = check_perfect_match.values_list('action', flat=True)[0]

            matching_command = check_perfect_match[0]
            serializer = CommandSerializer(matching_command)
            return Response(serializer.data)

        # If there is no perfect match, then use NLP to guess the right answer
        else:
            print("\nUsing NLP\n")

            message_token = nlp(input_command)

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

            # This is the action to take
            action = matching_command.action

            serializer = CommandSerializer(matching_command)
            return Response(serializer.data)

    def post(self):
        print(self.request.POST.get('test_val'))
        return Response("I think it worked")
